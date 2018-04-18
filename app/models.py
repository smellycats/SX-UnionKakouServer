# -*- coding: utf-8 -*-
import arrow

from . import db


class Traffic(db.Model):
    """过车信息"""
    __bind_key__ = 'kakou'
    __tablename__ = 'traffic_vehicle_pass'
    pass_id = db.Column(db.Integer, primary_key=True)
    crossing_id = db.Column(db.Integer)
    lane_no = db.Column(db.Integer)
    direction_index = db.Column(db.Integer)
    plate_no = db.Column(db.String(20), default='-')
    plate_type = db.Column(db.String(10))
    pass_time = db.Column(db.DateTime)
    vehicle_speed = db.Column(db.Integer)
    vehicle_len = db.Column(db.Integer, default=0)
    plate_color = db.Column(db.String(10))
    vehicle_color = db.Column(db.String(10))
    vehicle_type = db.Column(db.String(10))
    vehicle_color_depth = db.Column(db.String(10))
    plate_state = db.Column(db.String(10), default='0')
    image_path = db.Column(db.String(256), default='')
    plate_image_path = db.Column(db.String(256), default='')
    tfs_id = db.Column(db.Integer, default=0)
    vehicle_state = db.Column(db.Integer, default=0)
    vehicle_info_level = db.Column(db.Integer, default=1)
    vehicle_logo = db.Column(db.Integer)
    vehicle_sublogo = db.Column(db.Integer)
    vehicle_model = db.Column(db.Integer)
    pilotsunvisor = db.Column(db.Integer, default=0)
    

    def __init__(self, crossing_id, lane_no, direction_index, plate_no,
                 plate_type, pass_time, vehicle_speed=0, vehicle_len=0,
                 plate_color='0', vehicle_color='Z', vehicle_type='X99',
                 vehicle_color_depth='',
                 plate_state='0', image_path='', plate_image_path='', tfs_id=0,
                 vehicle_state=0, vehicle_info_level=1, vehicle_logo=None,
                 vehicle_sublogo=None, vehicle_model=None, pilotsunvisor=0):
        self.crossing_id = crossing_id
        self.lane_no = lane_no
        self.direction_index = direction_index
        self.plate_no = plate_no
        self.plate_type = plate_type
        self.pass_time = pass_time
        self.vehicle_speed = vehicle_speed
        self.vehicle_len = vehicle_len
        self.plate_color = plate_color
        self.vehicle_color = vehicle_color
        self.vehicle_type = vehicle_type
        self.vehicle_color_depth = vehicle_color_depth
        self.plate_state = plate_state
        self.image_path = image_path
        self.plate_image_path = plate_image_path
        self.tfs_id = tfs_id
        self.vehicle_state = vehicle_state
        self.vehicle_info_level = vehicle_info_level
        self.vehicle_logo = vehicle_logo
        self.vehicle_sublogo = vehicle_sublogo
        self.vehicle_model = vehicle_model
        self.pilotsunvisor = pilotsunvisor

    def __repr__(self):
        return '<Traffic %r>' % self.pass_id


class TrafficDispositionVehicle(db.Model):
    """布控车辆信息"""
    __bind_key__ = 'kakou'
    __tablename__ = 'traffic_disposition_vehicle'
    disposition_id = db.Column(db.Integer, primary_key=True)
    disposition_index = db.Column(db.String(32))
    disposition_type = db.Column(db.String(10))
    control_unit_id = db.Column(db.Integer)
    disposition_nature = db.Column(db.String(10))
    disposition_reason = db.Column(db.String(10))
    priority = db.Column(db.String(10))
    plate_no = db.Column(db.String(15))
    plate_color = db.Column(db.String(10))
    vehicle_color = db.Column(db.String(10))
    vehicle_type = db.Column(db.String(10))
    plate_type = db.Column(db.String(10))
    disposition_start_time = db.Column(db.DateTime)
    disposition_stop_time = db.Column(db.DateTime)
    contact_tel = db.Column(db.String(32))
    alarm_plan = db.Column(db.String(256))
    region_code = db.Column(db.String(15))
    identify = db.Column(db.String(10))
    disposition_remark = db.Column(db.String(256))
    user_id = db.Column(db.Integer)
    create_time = db.Column(db.DateTime)
    modify_time = db.Column(db.DateTime)
    check_user_id = db.Column(db.Integer)
    check_time = db.Column(db.DateTime)
    check_remark = db.Column(db.String(256))
    check_result = db.Column(db.String(10))
    status = db.Column(db.String(10))
    del_flag = db.Column(db.Integer)
    

    def __init__(self, disposition_id, disposition_index, disposition_type, control_unit_id,
                 disposition_nature, disposition_reason, priority, plate_no, plate_color,
		 vehicle_color, vehicle_type, plate_type, disposition_start_time,
		 disposition_stop_time, contact_tel, alarm_plan, region_code, identify,
		 disposition_remark, user_id, create_time, modify_time, check_user_id,
		 check_time, check_remark, check_result, status, del_flag=0):
        self.disposition_id = disposition_id
        self.disposition_index = disposition_index
        self.disposition_type = disposition_type
        self.control_unit_id = control_unit_id
        self.disposition_nature = disposition_nature
        self.disposition_reason = disposition_reason
        self.priority = priority
        self.plate_no = plate_no
        self.plate_color = plate_color
        self.vehicle_color = vehicle_color
	self.vehicle_type = vehicle_type
	self.plate_type = plate_type
	self.disposition_start_time = disposition_start_time
	self.disposition_stop_time = disposition_stop_time
	self.contact_tel = contact_tel
	self.alarm_plan = alarm_plan
	self.region_code = region_code
	self.identify = identify
	self.disposition_remark = disposition_remark
	self.user_id = user_id
	self.create_time = create_time
	self.modify_time = modify_time
	self.check_user_id = check_user_id
	self.check_time = check_time
	self.check_remark = check_remark
	self.check_result = check_result
	self.status = status
	self.del_flag = del_flag

    def __repr__(self):
        return '<TrafficDispositionVehicle %r>' % self.disposition_id


class TrafficCrossingInfo(db.Model):
    """卡口地点信息"""
    __bind_key__ = 'kakou'
    __tablename__ = 'traffic_crossing_info'
    crossing_id = db.Column(db.Integer, primary_key=True)
    crossing_index = db.Column(db.String(32))
    control_unit_id = db.Column(db.Integer)
    crossing_name = db.Column(db.String(64))
    driveway_num = db.Column(db.Integer)
    cross_type = db.Column(db.String(10))
    speed_limit = db.Column(db.Integer)
    logo_speed_limit = db.Column(db.Integer)
    direction_num = db.Column(db.Integer)
    inside_index = db.Column(db.Integer)

    def __init__(self, crossing_index, control_unit_id, crossing_name, driveway_num,
		 cross_type,speed_limit, logo_speed_limit, direction_num, inside_index):
	self.crossing_index = crossing_index
        self.control_unit_id = control_unit_id
        self.corssing_name = crossing_name
	self.driveway_num = driveway_num
	self.cross_type = cross_type
	self.speed_limit = speed_limit
	self.logo_speed_limit = logo_speed_limit
	self.direction_num = direction_num
        self.inside_index = inside_index

    def __repr__(self):
        return '<TrafficCrossingInfo %r>' % self.crossing_id


class TrafficDirectionInfo(db.Model):
    """"方向信息"""
    __bind_key__ = 'kakou'
    __tablename__ = 'traffic_direction_info'
    direction_id = db.Column(db.Integer, primary_key=True)
    direction_index = db.Column(db.Integer)
    direction_name = db.Column(db.String(64))
    crossing_id = db.Column(db.Integer)
    del_flag = db.Column(db.Integer)
    res_num1 = db.Column(db.Integer)
    res_num2 = db.Column(db.Integer)
    res_str1 = db.Column(db.String(64))
    res_str2 = db.Column(db.String(64))
    flow_threshold = db.Column(db.String(30))

    def __init__(self, direction_index, direction_name, crossing_id, del_flag,
		 res_num1, res_num2, res_str1, res_str2, flow_threshold):
	self.direction_index = direction_index
        self.direction_name = direction_name
        self.crossing_id = crossing_id
	self.del_flag = del_flag
	self.res_num1 = res_num1
	self.res_num2 = res_num2
	self.res_str1 = res_str1
	self.res_str2 = res_str2
        self.flow_threshold = flow_threshold

    def __repr__(self):
        return '<TrafficDirectionInfo %r>' % self.direction_id


class TrafficLaneInfo(db.Model):
    """"车道信息"""
    __bind_key__ = 'kakou'
    __tablename__ = 'traffic_lane_info'
    lane_id = db.Column(db.Integer, primary_key=True)
    lane_no = db.Column(db.Integer)
    lane_name = db.Column(db.String(64))
    camera_ip = db.Column(db.String(64))
    camera_port = db.Column(db.Integer)
    device_id = db.Column(db.Integer)
    channel_no = db.Column(db.Integer)
    enable = db.Column(db.Integer)
    crossing_id = db.Column(db.Integer)
    modify_date = db.Column(db.DateTime)
    direction_id = db.Column(db.Integer)
    

    def __init__(self, lane_id, lane_no, lane_name, camera_ip, camera_port,
		 device_id, channel_no, enable, crossing_id, modify_date,
		 direction_id):
	self.lane_id = lane_id
        self.lane_no = lane_no
        self.lane_name = lane_name
	self.camera_ip = camera_ip
	self.camera_port = camera_port
	self.device_id = device_id
	self.channel_no = channel_no
	self.enable = enable
        self.crossing_id = crossing_id
	self.modify_date = modify_date
	self.direction_id = direction_id

    def __repr__(self):
        return '<TrafficLaneInfo %r>' % self.lane_id


class ControlUnit(db.Model):
    """控制单元"""
    __bind_key__ = 'kakou'
    __tablename__ = 'control_unit'
    control_unit_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    parent_id = db.Column(db.Integer)
    unit_level = db.Column(db.Integer)

    def __init__(self, control_unit_id, name, parent_id, unit_level):
        self.control_unit_id = control_unit_id
        self.name = name
	self.parent_id = parent_id
	self.unit_level = unit_level

    def __repr__(self):
        return '<ControlUnit %r>' % self.control_unit_id


class TrafficDispositionAlarm(db.Model):
    """布控报警信息配置"""
    __bind_key__ = 'kakou'
    __tablename__ = 'traffic_disposition_alarm'
    disposition_alarm_id = db.Column(db.Integer, primary_key=True)
    disposition_type = db.Column(db.String(10))
    disposition_id = db.Column(db.Integer)
    disposition_reason = db.Column(db.String(10))
    crossing_id = db.Column(db.Integer)
    lane_no = db.Column(db.Integer)
    direction_index = db.Column(db.Integer)
    pass_time = db.Column(db.DateTime)
    plate_no = db.Column(db.String(15))
    plate_type = db.Column(db.String(10))
    plate_color = db.Column(db.String(10))

    def __init__(self, disposition_alarm_id, disposition_type, disposition_id,
                 disposition_reason, crossing_id, lane_no, direction_index,
                 pass_time, plate_no, plate_type, plate_color):
        self.disposition_alarm_id = disposition_alarm_id
        self.disposition_type = disposition_type
        self.disposition_id = disposition_id
        self.disposition_reason = disposition_reason
        self.crossing_id = crossing_id
        self.lane_no = lane_no
        self.direction_index = direction_index
        self.pass_time = pass_time
        self.plate_no = plate_no
        self.plate_type = plate_type
        self.plate_color = plate_color

    def __repr__(self):
        return '<TrafficDispositionAlarm %r>' % self.disposition_alarm_id


class TrafficDispositionContact(db.Model):
    """布控联系人配置"""
    __bind_key__ = 'kakou'
    __tablename__ = 'traffic_disposition_contact'
    contact_id = db.Column(db.Integer, primary_key=True)
    disposition_id = db.Column(db.Integer)
    contact_name = db.Column(db.String(64))
    contact_type = db.Column(db.Integer)
    contact_tel = db.Column(db.String(15))
    contact_email = db.Column(db.String(64))
    modify_date = db.Column(db.DateTime)
    del_flag = db.Column(db.Integer)
    sms_contact_phone = db.Column(db.String(1000))

    def __init__(self, disposition_id, contact_name, contact_type, contact_tel,
                 contact_email, modify_date, del_flag, sms_contact_phone):
        self.disposition_id = disposition_id
        self.contact_name = contact_name
        self.contact_type = contact_type
        self.contact_tel = contact_tel
        self.contact_email = contact_email
        self.modify_date = modify_date
        self.del_flag = del_flag
	self.sms_contact_phone = sms_contact_phone

    def __repr__(self):
        return '<TrafficDispositionContact %r>' % self.contact_id
