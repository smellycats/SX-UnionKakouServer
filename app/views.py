# -*- coding: utf-8 -*-
import json

import arrow
from flask import g, request, make_response, jsonify, abort
from sqlalchemy import func

from . import db, app, logger, access_logger
from models import *
#import helper


@app.route('/')
def index_get():
    result = {
        'alarm_url': '%salarm{/alarm_id}' % (request.url_root),
        'stat4_url': '%sstat?q={}' % (request.url_root),
        'control_unit_url': '%scontrol_unit{/control_unit_id}' % (request.url_root),
        'traffic_crossing_info_url': '%straffic_crossing_info{/crossing_id}' % (request.url_root),
        'traffic_direction_info_url': '%straffic_direction_info{/corssing_id}' % (request.url_root),
        'traffic_lane_info_url': '%straffic_lane_info{/direction_id}' % (request.url_root)
    }
    header = {'Cache-Control': 'public, max-age=60, s-maxage=60'}
    return jsonify(result), 200, header


@app.route('/alarm_maxid', methods=['GET'])
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


@app.route('/alarm/maxid', methods=['GET'])
def alarm_maxid2_get():
    try:
        q = db.session.query(func.max(TrafficDispositionAlarm.disposition_alarm_id)).first()
        return jsonify({'maxid': q[0]}), 200
    except Exception as e:
        logger.error(e)
        raise


@app.route('/alarm/<int:alarm_id>', methods=['GET'])
def alarm_get(alarm_id):
    try:
        t = TrafficDispositionAlarm.query.filter_by(disposition_alarm_id=alarm_id).first()
        if t is None:
            return jsonify({}), 404
        t2 = TrafficDispositionVehicle.query.filter_by(disposition_id=t.disposition_id).first()
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
        return jsonify(item), 200
    except Exception as e:
        logger.exception(e)
        raise


@app.route('/kkdd/<int:kkdd_id>', methods=['GET'])
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


@app.route('/stat4', methods=['GET'])
def stat4_get():
    try:
        st = request.args.get('st', None)
        et = request.args.get('et', None)
        crossing_id = request.args.get('crossing_id', None)
        direction_index = request.args.get('direction_index', None)
        t = db.session.query(Traffic).filter(Traffic.pass_time >= st, Traffic.pass_time <= et)
        if crossing_id is not None:
            t = t.filter(Traffic.crossing_id == crossing_id)
        if direction_index is not None:
            t = t.filter(Traffic.direction_index == direction_index)
        return jsonify({'count': t.count()}), 200
    except Exception as e:
        logger.exception(e)
        raise


@app.route('/control_unit', methods=['GET'])
def control_unit_all_get():
    try:
        t = ControlUnit.query.filter_by().all()
        items = []
        for i in t:
            item = {
                'id': i.control_unit_id,
                'name': i.name,
                'parent_id': i.parent_id,
                'unit_level': i.unit_level
            }
            items.append(item)
        return jsonify({'total_count': len(items), 'items': items}), 200
    except Exception as e:
        logger.error(e)
        raise


@app.route('/control_unit/<int:control_unit_id>', methods=['GET'])
def control_unit_get(control_unit_id):
    try:
        i = ControlUnit.query.filter_by(control_unit_id=control_unit_id).first()
        if i is None:
             return jsonify({}), 404
        item = {
            'id': i.control_unit_id,
            'name': i.name,
            'parent_id': i.parent_id,
            'unit_level': i.unit_level
        }
        return jsonify(item), 200
    except Exception as e:
        logger.error(e)
        raise


@app.route('/traffic_crossing_info', methods=['GET'])
def traffic_crossing_info_all_get():
    q = request.args.get('q', None)
    if q is None:
        abort(400)
    try:
        args = json.loads(q)
    except Exception as e:
        logger.error(e)
        abort(400)
    try:
        limit = int(args.get('per_page', 20))
        offset = (int(args.get('page', 1)) - 1) * limit
        s = db.session.query(TrafficCrossingInfo)
        if args.get('control_unit_id', None) is not None:
            s = s.filter(TrafficCrossingInfo.control_unit_id == args['control_unit_id'])
        if args.get('crossing_index', None) is not None:
            s = s.filter(TrafficCrossingInfo.crossing_index == args['crossing_index'])
        result = s.limit(limit).offset(offset).all()
        # 总数
        total = s.count()
        # 结果集为空
        if len(result) == 0:
            return jsonify({'total_count': total, 'items': []}), 200

        items = []
        for i in result:
            item = {
                'crossing_id': i.crossing_id,
                'crossing_index': i.crossing_index,
                'control_unit_id': i.control_unit_id,
                'crossing_name': i.crossing_name,
                'driveway_num': i.driveway_num,
                'cross_type': i.cross_type,
                'direction_num': i.direction_num,
                'inside_index': i.inside_index
            }
            items.append(item)
        return jsonify({'total_count': total, 'items': items}), 200
    except Exception as e:
        logger.error(e)
        raise


@app.route('/traffic_crossing_info/<int:crossing_id>', methods=['GET'])
def traffic_crossing_info_get(crossing_id):
    try:
        i = TrafficCrossingInfo.query.filter_by(crossing_id=crossing_id).first()
        if i is None:
            return jsonify({}), 404
        item = {
            'crossing_id': i.crossing_id,
            'crossing_index': i.crossing_index,
            'control_unit_id': i.control_unit_id,
            'crossing_name': i.crossing_name,
            'driveway_num': i.driveway_num,
            'cross_type': i.cross_type,
            'direction_num': i.direction_num,
            'inside_index': i.inside_index
        }
        return jsonify(item), 200
    except Exception as e:
        logger.error(e)
        raise


@app.route('/traffic_direction_info/<int:crossing_id>', methods=['GET'])
def traffic_direction_info_get(crossing_id):
    try:
        fxbh2 = {u'IN': 9, u'OT': 10, u'WE': 2, u'EW': 1, u'SN': 3, u'NS': 4}
        fxbh = {9: u'IN', 10: u'OT', 2: u'WE', 1: u'EW', 3: u'SN', 4: u'NS'}
        t = TrafficDirectionInfo.query.filter_by(crossing_id=crossing_id).all()
        items = []
        for i in t:
            item = {
                'direction_id': i.direction_id,
                'direction_name': i.direction_name,
                'direction_index': i.direction_index,
                'fxbh_code': fxbh.get(i.direction_index, u'QT')
            }
	    items.append(item)
        return jsonify({'total_count': len(items), 'items': items}), 200
    except Exception as e:
        logger.error(e)
        raise


@app.route('/traffic_lane_info/<int:direction_id>', methods=['GET'])
def traffic_lane_info_get(direction_id):
    try:
        t = TrafficLaneInfo.query.filter_by(crossing_id=direction_id).all()
        items = []
        for i in t:
            item = {
                'lane_id': i.lane_id,
                'lane_no': i.lane_no,
                'crossing_id': i.crossing_id
            }
            items.append(item)
        return jsonify({'total_count': len(items), 'items': items}), 200
    except Exception as e:
        logger.error(e)
        raise

