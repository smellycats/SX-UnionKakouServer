# -*- coding: utf-8 -*-
import arrow

from app import app, db
from app.models import *
from app.helper import *


def test_scope_get():
    scope = Scope.query.all()
    for i in scope:
        print i.name

def test_user_get():
    user = Users.query.filter_by(username='admin', banned=0).first()
    print user.scope
    
def test_traffic_get():
    r = Traffic.query.first()
    #help(r)
    print r
    #print type(r.pass_time)
    #print r.crossing_id

def test_traffic_add():
    t_list = []
    for i in range(3):
        t = Traffic(crossing_id='441302123', lane_no=1, direction_index='IN',
                    plate_no=u'粤L12345', plate_type='',
                    pass_time='2015-12-13 01:23:45', plate_color='0')
        db.session.add(t)
        t_list.append(t)
    help(db.session.__call__)
    #db.session.commit()
    #r = [{'pass_id': r.pass_id} for r in t_list]
    #print r

def test_traffic_add2():
    vals = [
	u"('441302123', 1, 'IN', '粤L12345', '', '2015-12-13 01:23:45', '0')",
	u"('441302123', 1, 'IN', '粤L12345', '', '2015-12-13 01:23:45', '0')"
    ]
    print vals
    #print ','.join(vals)
    sql = ("insert into traffic(crossing_id, lane_no, direction_index, plate_no, plate_type, pass_time, plate_color) values %s") % ','.join(vals)
    query = db.get_engine(app, bind='kakou').execute(sql)
    query.close()

def test_stat():
    st = '2017-03-20 12:00:00'
    et = '2017-03-20 13:00:00'
    kkdd = 441302001
    sql = ("select count(*) from traffic_vehicle_pass where pass_time >='{0}' and pass_time <='{1}' and crossing_id = {2}".format(st, et, kkdd))
    query = db.get_engine(app, bind='kakou').execute(sql)
    r = query.fetchone()[0]
    print r

def test_stat2():
    st = '2017-03-20 12:00:00'
    et = '2017-03-20 13:00:00'
    kkdd = 441302001
    t = db.session.query(Traffic).filter(Traffic.pass_time >= st)
    t = t.filter(Traffic.pass_time <= et)
    t = t.filter(Traffic.crossing_id == kkdd)
    t = t.count()
    print t

def test_user_add():
    # u = UserTest(name='fire')
    #db.session.add(u)
    #db.session.commit()
    name = 'fire'
    sql = ("insert into test_user(name) values('%s'),('feizi')") % name
    query = db.get_engine(app, bind='kakou').execute(sql)
    query.close()

def test_traffic_crossing_info():
    t = TrafficCrossingInfo.query.filter_by(inside_index=441302001).first()
    print t.control_unit_id

def test_control_unit():
    t = ControlUnit.query.filter_by(control_unit_id=2).first()
    print t.control_unit_id

def test_alarm():
    t = TrafficDispositionAlarm.query.filter_by(control_unit_id=2).first()
    print t.control_unit_id

def test_alarm2():
    sql = ("select max(disposition_alarm_id) from traffic_disposition_alarm")
    query = db.get_engine(app, bind='kakou').execute(sql)
    print query.fetchone()[0]
    query.close()

def test_traffic_info():
    t = TrafficDispositionAlarm.query.filter_by(disposition_alarm_id=143).first()
    print t

def test_traffic_dis_vehicle():
    t = TrafficDispositionVehicle.query.filter_by(disposition_id=10, check_result='1', status='2').first()
    print t

def test_traffic_dis_contact():
    t = TrafficDispositionContact.query.filter_by(disposition_id = 18).all()
    print t
    for i in t:
    	print (i.contact_tel,)

def test10():
    sql = ("select * from traffic_disposition_contact")
    query = db.get_engine(app, bind='kakou').execute(sql)
    query.close()
    print query.fetchone()

def test11():
    kkdd_id = 441302001
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
    print item

if __name__ == '__main__':
    test_stat2()

