# -*- coding: utf-8 -*-
import json
from functools import wraps

import arrow
from flask import g, request, make_response, jsonify, abort
from flask_restful import reqparse, abort, Resource
from passlib.hash import sha256_crypt
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from . import db, app, auth, limiter, logger, access_logger
from models import *
import helper


@app.route('/')
@limiter.limit("5000/hour")
def index_get():
    result = {
        'user_url': 'http://%suser{/user_id}' % (request.url_root),
        'kakou_url': 'http://%skakou/' % (request.url_root)
    }
    header = {'Cache-Control': 'public, max-age=60, s-maxage=60'}
    return jsonify(result), 200, header


@app.route('/alarm_maxid', methods=['GET'])
@limiter.exempt
def alarm_maxid_get():
    try:
	sql = ("select max(disposition_alarm_id) from traffic_disposition_alarm")
	query = db.get_engine(app, bind='kakou').execute(sql)
        maxid = query.fetchone()[0]
	query.close()
    except Exception as e:
        logger.error(e)
        raise
    
    return jsonify({'maxid': maxid}), 200


@app.route('/alarm/<int:alarm_id>', methods=['GET'])
@limiter.exempt
def alarm_get(alarm_id):
    try:
	t = TrafficDispositionAlarm.query.filter_by(disposition_alarm_id=alarm_id).first()
	if t is None:
	    return jsonify({}), 404
	t2 = TrafficDispositionVehicle.query.filter_by(disposition_id=t.disposition_id, check_result='1', status='2').first()
	if t2 is None:
	    return jsonify({}), 404
	t3 = TrafficDispositionContact.query.filter_by(disposition_id=t.disposition_id).all()
	mobiles = []
	for i in t3:
	    mobiles.append(i.contact_tel)
	    if i.sms_contact_phone is not None and i.sms_contact_phone != '':
	        m = i.sms_contact_phone.split(',')
	        for j in m:
		    mobiles.append(j.strip())
	item = {
	    'disposition_type': t.disposition_type,
	    'disposition_reason': t.disposition_reason,
	    'disposition_id': t.disposition_id,
	    'crossing_id': t.crossing_id,
	    'lane_no': t.lane_no,
	    'direction_index': t.direction_index,
	    'pass_time': str(t.pass_time),
	    'plate_no': t.plate_no,
	    'plate_color': t.plate_color,
	    'mobiles': list(set(mobiles)),
	    'start_time': str(t2.disposition_start_time),
	    'stop_time': str(t2.disposition_stop_time)
	}
    except Exception as e:
        logger.exception(e)
        raise
    
    return jsonify(item), 200


@app.route('/kkdd/<int:kkdd_id>', methods=['GET'])
@limiter.exempt
def kkdd_get(kkdd_id):
    try:
	t = TrafficCrossingInfo.query.filter_by(inside_index=kkdd_id).first()
	if t is None:
	    return jsonify({}), 404
	t2 = ControlUnit.query.filter_by(control_unit_id=t.control_unit_id).first()
	item = {
	    'control_unit_id': t.control_unit_id,
	    'kkdd_id': t.inside_index,
	    'kkdd_name': t.crossing_name,
	    'city_name': t2.name
	}
    except Exception as e:
        logger.exception(e)
        raise
    
    return jsonify(item), 200


@app.route('/traffic/<string:st>/<string:et>/<int:kkdd>', methods=['GET'])
@limiter.exempt
def traffic_get(st, et, kkdd):
    try:
        r = db.session.query(Traffic).filter(
	    Traffic.pass_time>=st, Traffic.pass_time<et, Traffic.crossing_id>=kkdd, Traffic.crossing_id<kkdd+100).all()
        items = []
	for i in r:
	    item = {}
	    item['id'] = i.pass_id
	    hphm = i.plate_no
	    if i.plate_no is None or i.plate_no == '':
	        hphm = '-'
	    item['hphm'] = hphm
	    item['jgsj'] = str(i.pass_time)
	    item['kkdd'] = i.crossing_id
	    item['imgurl'] = i.image_path
	    items.append(item)
    except Exception as e:
        logger.exception(e)
        raise
    
    return jsonify({'total_count': len(items), 'items': items}), 200


@app.route('/stat/<string:st>/<string:et>/<int:kkdd>', methods=['GET'])
@limiter.exempt
def stat_get(st, et, kkdd):
    try:
        sql = ("select count(*) from traffic_vehicle_pass where pass_time >='{0}' and pass_time <='{1}' and crossing_id >= {2} and crossing_id < {3}".format(st, et, kkdd, kkdd+100))
        query = db.get_engine(app, bind='kakou').execute(sql)
        r = query.fetchone()[0]
    except Exception as e:
        logger.exception(e)
        raise
    
    return jsonify({'count': r}), 200


@app.route('/stat2/<string:st>/<string:et>/<int:kkdd>', methods=['GET'])
@limiter.exempt
def stat2_get(st, et, kkdd):
    try:
        sql = ("select count(*) from traffic_vehicle_pass where pass_time >='{0}' and pass_time <='{1}' and crossing_id = {2}".format(st, et, kkdd))
        query = db.get_engine(app, bind='kakou').execute(sql)
        r = query.fetchone()[0]
    except Exception as e:
        logger.exception(e)
        raise
    
    return jsonify({'count': r}), 200


@app.route('/stat3', methods=['GET'])
@limiter.exempt
def stat3_get():
    try:
        st = request.args.get('st', None)
        et = request.args.get('et', None)
        kkdd = request.args.get('kkdd', None)
        fxbh = request.args.get('fxbh', None)
        t = db.session.query(Traffic).filter(Traffic.pass_time >= st, Traffic.pass_time <= et)
	if kkdd is not None:
            t = t.filter(Traffic.crossing_id == kkdd)
	if fxbh is not None:
	    t = t.filter(Traffic.direction_index == fxbh)
        r = t.count()
    except Exception as e:
        logger.exception(e)
        raise
    
    return jsonify({'count': r}), 200


@app.route('/control_unit', methods=['GET'])
@limiter.exempt
def control_unit_get():
    try:
	t = ControlUnit.query.filter_by().all()
	items = []
        for i in t:
	    item = {}
	    item['id'] = i.control_unit_id
	    item['name'] = i.name
	    item['parent_id'] = i.parent_id
	    item['unit_level'] = i.unit_level
	    items.append(item)
        return jsonify({'total_count': len(items), 'items': items}), 200
    except Exception as e:
        logger.error(e)
        raise


@app.route('/traffic_crossing_info', methods=['GET'])
@limiter.exempt
def traffic_crossing_info_all_get():
    try:
	t = TrafficCrossingInfo.query.filter_by().all()
	items = []
        for i in t:
	    item = {}
	    item['id'] = i.crossing_id
	    item['kkdd_id'] = i.inside_index
	    item['kkdd_name'] = i.crossing_name
	    item['fxbh_num'] = i.direction_num
	    item['lane_num'] = i.driveway_num
	    items.append(item)
    except Exception as e:
        logger.error(e)
        raise
    
    return jsonify({'total_count': len(items), 'items': items}), 200


@app.route('/traffic_crossing_info/<int:unit_id>', methods=['GET'])
@limiter.exempt
def traffic_crossing_info_get(unit_id):
    try:
	t = TrafficCrossingInfo.query.filter_by(control_unit_id=unit_id).all()
	items = []
        for i in t:
	    item = {}
	    item['id'] = i.crossing_id
	    item['kkdd_id'] = i.inside_index
	    item['kkdd_name'] = i.crossing_name
	    item['fxbh_num'] = i.direction_num
	    item['lane_num'] = i.driveway_num
	    items.append(item)
    except Exception as e:
        logger.error(e)
        raise
    
    return jsonify({'total_count': len(items), 'items': items}), 200


@app.route('/traffic_direction_info/<int:crossing_id>', methods=['GET'])
@limiter.exempt
def traffic_direction_info_get(crossing_id):
    try:
	fxbh2 = {u'IN': 9, u'OT': 10, u'WE': 2, u'EW': 1, u'SN': 3, u'NS': 4}
	fxbh = {9: u'IN', 10: u'OT', 2: u'WE', 1: u'EW', 3: u'SN', 4: u'NS'}
	t = TrafficDirectionInfo.query.filter_by(crossing_id=crossing_id).all()
	items = []
        for i in t:
	    item = {}
	    item['id'] = i.direction_id
	    item['fxbh_name'] = i.direction_name
	    item['fxbh_id'] = i.direction_index
	    item['fxbh_code'] = fxbh.get(i.direction_index, u'QT')
	    items.append(item)
    except Exception as e:
        logger.error(e)
        raise
    
    return jsonify({'total_count': len(items), 'items': items}), 200


@app.route('/traffic_lane_info/<int:direction_id>', methods=['GET'])
@limiter.exempt
def traffic_lane_info_get(direction_id):
    try:
	t = TrafficLaneInfo.query.filter_by(crossing_id=direction_id).all()
	items = []
        for i in t:
	    item = {}
	    item['id'] = i.lane_id
	    item['lane_no'] = i.lane_no
	    item['crossing_id'] = i.crossing_id
	    items.append(item)
    except Exception as e:
        logger.error(e)
        raise
    
    return jsonify({'total_count': len(items), 'items': items}), 200