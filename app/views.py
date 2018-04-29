# -*- coding: utf-8 -*-
import json

import arrow
from flask import g, request, make_response, jsonify, abort
from sqlalchemy import func

from . import db, app, logger, access_logger
from .models import *
#import helper


@app.route('/')
def index_get():
    result = {
        'alarm_url': '%salarm{/alarm_id}' % (request.url_root),
        'stat_url': '%sstat?q={}' % (request.url_root),
        'control_unit_url': '%scontrol_unit{/control_unit_id}' % (request.url_root),
        'traffic_crossing_info_url': '%straffic_crossing_info{/crossing_id}' % (request.url_root),
        'traffic_direction_info_url': '%straffic_direction_info{/corssing_id}' % (request.url_root),
        'traffic_lane_info_url': '%straffic_lane_info{/direction_id}' % (request.url_root)
    }
    header = {'Cache-Control': 'public, max-age=60, s-maxage=60'}
    return jsonify(result), 200, header


@app.route('/alarm/maxid', methods=['GET'])
def alarm_maxid_get():
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
            'stop_time': str(t2.disposition_stop_time),
            'disposition_reason': t2.disposition_reason,
            'res_str1': t2.res_str1,
            'res_str2': t2.res_str2
        }
        return jsonify(item), 200
    except Exception as e:
        logger.exception(e)
        raise


@app.route('/stat', methods=['GET'])
def stat_get():
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
        s = db.session.query(ControlUnit)
        if args.get('parent_id', None) is not None:
            s = s.filter(ControlUnit.parent_id == args['parent_id'])
        result = s.limit(limit).offset(offset).all()
        # 总数
        total = s.count()
        items = []
        for i in result:
            item = {
                'id': i.control_unit_id,
                'name': i.name,
                'parent_id': i.parent_id,
                'unit_level': i.unit_level
            }
            items.append(item)
        return jsonify({'total_count': total, 'items': items}), 200
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
        logger.exception(e)
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


@app.route('/traffic_direction_info', methods=['GET'])
def traffic_direction_info_all_get():
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
        s = db.session.query(TrafficDirectionInfo)
        if args.get('crossing_id', None) is not None:
            s = s.filter(TrafficDirectionInfo.crossing_id == args['crossing_id'])
        result = s.limit(limit).offset(offset).all()
        # 总数
        total = s.count()
        # 结果集为空
        if len(result) == 0:
            return jsonify({'total_count': total, 'items': []}), 200

        items = []
        for i in result:
            item = {
                'direction_id': i.direction_id,
                'direction_name': i.direction_name,
                'direction_index': i.direction_index,
                'crossing_id': i.crossing_id
            }
            items.append(item)
        return jsonify({'total_count': total, 'items': items}), 200
    except Exception as e:
        logger.exception(e)
        raise


@app.route('/traffic_direction_info/<int:direction_id>', methods=['GET'])
def traffic_direction_info_get(direction_id):
    try:
        i = TrafficDirectionInfo.query.filter_by(direction_id=direction_id).first()
        if i is None:
             return jsonify({}), 404
        item = {
            'direction_id': i.direction_id,
            'direction_name': i.direction_name,
            'direction_index': i.direction_index,
            'crossing_id': i.crossing_id
        }
        return jsonify(item), 200
    except Exception as e:
        logger.error(e)
        raise


@app.route('/traffic_lane_info', methods=['GET'])
def traffic_lane_info_all_get():
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
        s = db.session.query(TrafficLaneInfo)
        if args.get('crossing_id', None) is not None:
            s = s.filter(TrafficLaneInfo.crossing_id == args['crossing_id'])
        if args.get('direction_id', None) is not None:
            s = s.filter(TrafficLaneInfo.direction_id == args['direction_id'])
        result = s.limit(limit).offset(offset).all()
        # 总数
        total = s.count()
        # 结果集为空
        if len(result) == 0:
            return jsonify({'total_count': total, 'items': []}), 200

        items = []
        for i in result:
            item = {
                'lane_id': i.lane_id,
                'lane_no': i.lane_no,
                'lane_name': i.lane_name,
                'camera_ip': i.camera_ip,
                'camera_port': i.camera_port,
                'device_id': i.device_id,
                'crossing_id': i.crossing_id,
                'modify_date': i.modify_date.strftime('%Y-%m-%d %H:%M:%S'),
                'direction_id': i.direction_id
            }
            items.append(item)
        return jsonify({'total_count': total, 'items': items}), 200
    except Exception as e:
        logger.exception(e)
        raise


@app.route('/traffic_lane_info/<int:lane_id>', methods=['GET'])
def traffic_lane_info_get(lane_id):
    try:
        i = TrafficLaneInfo.query.filter_by(lane_id=lane_id).first()
        if i is None:
             return jsonify({}), 404
        item = {
            'lane_id': i.lane_id,
            'lane_no': i.lane_no,
            'lane_name': i.lane_name,
            'camera_ip': i.camera_ip,
            'camera_port': i.camera_port,
            'device_id': i.device_id,
            'crossing_id': i.crossing_id,
            'modify_date': i.modify_date.strftime('%Y-%m-%d %H:%M:%S'),
            'direction_id': i.direction_id
        }
        return jsonify(item), 200
    except Exception as e:
        logger.error(e)
        raise


@app.route('/traffic_sysdict', methods=['GET'])
def traffic_sysdict_all_get():
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
        s = db.session.query(TrafficSysdict)
        if args.get('sysdict_type', None) is not None:
            s = s.filter(TrafficSysdict.sysdict_type == args['sysdict_type'])
        if args.get('sysdict_code', None) is not None:
            s = s.filter(TrafficSysdict.sysdict_code == args['sysdict_code'])
        result = s.limit(limit).offset(offset).all()
        # 总数
        total = s.count()
        # 结果集为空
        if len(result) == 0:
            return jsonify({'total_count': total, 'items': []}), 200

        items = []
        for i in result:
            item = {
                'sysdict_id': i.sysdict_id,
                'sysdict_type': i.sysdict_type,
                'sysdict_code': i.sysdict_code,
                'sysdict_name': i.sysdict_name,
                'sysdict_memo': i.sysdict_memo,
                'flag': i.flag,
                'show_order': i.show_order,
                'enable': i.enable,
                'change_code': i.change_code
            }
            items.append(item)
        return jsonify({'total_count': total, 'items': items}), 200
    except Exception as e:
        logger.exception(e)
        raise


@app.route('/traffic_sysdict/<int:sysdict_id>', methods=['GET'])
def traffic_sysdict_get(sysdict_id):
    try:
        i = TrafficSysdict.query.filter_by(sysdict_id=sysdict_id).first()
        if i is None:
             return jsonify({}), 404
        item = {
            'sysdict_id': i.sysdict_id,
            'sysdict_type': i.sysdict_type,
            'sysdict_code': i.sysdict_code,
            'sysdict_name': i.sysdict_name,
            'sysdict_memo': i.sysdict_memo,
            'flag': i.flag,
            'show_order': i.show_order,
            'enable': i.enable,
            'change_code': i.change_code
        }
        return jsonify(item), 200
    except Exception as e:
        logger.error(e)
        raise
