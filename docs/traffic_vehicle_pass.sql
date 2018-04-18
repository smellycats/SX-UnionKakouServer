/*
Navicat PGSQL Data Transfer

Source Server         : postgres
Source Server Version : 90405
Source Host           : localhost:5432
Source Database       : cms
Source Schema         : postgres

Target Server Type    : PGSQL
Target Server Version : 90405
File Encoding         : 65001

Date: 2016-03-07 09:10:54
*/


-- ----------------------------
-- Table structure for traffic_vehicle_pass
-- ----------------------------
DROP TABLE IF EXISTS "postgres"."traffic_vehicle_pass";
CREATE TABLE "postgres"."traffic_vehicle_pass" (
"pass_id" int4 DEFAULT nextval('traffic_vehicle_pass_pass_id_seq'::regclass) NOT NULL,
"crossing_id" int4,
"lane_no" int2,
"direction_index" int2,
"plate_no" varchar(20) COLLATE "default",
"plate_type" varchar(10) COLLATE "default",
"pass_time" timestamp(6),
"vehicle_speed" int2,
"vehicle_len" int2,
"plate_color" varchar(10) COLLATE "default",
"vehicle_color" varchar(10) COLLATE "default",
"vehicle_type" varchar(10) COLLATE "default",
"vehicle_color_depth" varchar(10) COLLATE "default",
"plate_state" varchar(10) COLLATE "default",
"image_path" varchar(256) COLLATE "default",
"plate_image_path" varchar(256) COLLATE "default",
"tfs_id" int4,
"vehicle_state" int4,
"res_num1" int4,
"res_num2" int4,
"res_str3" varchar(64) COLLATE "default",
"res_str4" varchar(64) COLLATE "default",
"vehicle_info_level" int2,
"vehicle_logo" int4,
"vehicle_sublogo" int4,
"vehicle_model" int4,
"pilotsunvisor" int2
)
WITH (OIDS=FALSE)

;
COMMENT ON TABLE "postgres"."traffic_vehicle_pass" IS '所有过车信息表';
COMMENT ON COLUMN "postgres"."traffic_vehicle_pass"."pass_id" IS '过车数据唯一标识';
COMMENT ON COLUMN "postgres"."traffic_vehicle_pass"."crossing_id" IS '路口';
COMMENT ON COLUMN "postgres"."traffic_vehicle_pass"."lane_no" IS '过车车道';
COMMENT ON COLUMN "postgres"."traffic_vehicle_pass"."direction_index" IS '方向编号';
COMMENT ON COLUMN "postgres"."traffic_vehicle_pass"."plate_no" IS '车牌号码';
COMMENT ON COLUMN "postgres"."traffic_vehicle_pass"."plate_type" IS '车牌类型';
COMMENT ON COLUMN "postgres"."traffic_vehicle_pass"."pass_time" IS '过车信息时间戳';
COMMENT ON COLUMN "postgres"."traffic_vehicle_pass"."vehicle_speed" IS '行车速度';
COMMENT ON COLUMN "postgres"."traffic_vehicle_pass"."vehicle_len" IS '车身长度';
COMMENT ON COLUMN "postgres"."traffic_vehicle_pass"."plate_color" IS '车牌颜色';
COMMENT ON COLUMN "postgres"."traffic_vehicle_pass"."vehicle_color" IS '车身颜色';
COMMENT ON COLUMN "postgres"."traffic_vehicle_pass"."vehicle_type" IS '车辆类型';
COMMENT ON COLUMN "postgres"."traffic_vehicle_pass"."vehicle_color_depth" IS '车身颜色深度';
COMMENT ON COLUMN "postgres"."traffic_vehicle_pass"."plate_state" IS '车牌状态(自动生成：0 正常/1 未识别处理：0 正常/2无车牌/3 非机动车4 残缺。。。)';
COMMENT ON COLUMN "postgres"."traffic_vehicle_pass"."image_path" IS '全景图片';
COMMENT ON COLUMN "postgres"."traffic_vehicle_pass"."plate_image_path" IS '车牌图片URL';
COMMENT ON COLUMN "postgres"."traffic_vehicle_pass"."tfs_id" IS '文件服务器ID';
COMMENT ON COLUMN "postgres"."traffic_vehicle_pass"."vehicle_state" IS '使用位运算，行驶状态（0-正常；1-嫌疑；2072-超速；2027-逆行等）';
COMMENT ON COLUMN "postgres"."traffic_vehicle_pass"."res_num1" IS '预留字段1';
COMMENT ON COLUMN "postgres"."traffic_vehicle_pass"."res_num2" IS '预留字段2';
COMMENT ON COLUMN "postgres"."traffic_vehicle_pass"."res_str3" IS '预留字段3';
COMMENT ON COLUMN "postgres"."traffic_vehicle_pass"."res_str4" IS '预留字段4';
COMMENT ON COLUMN "postgres"."traffic_vehicle_pass"."vehicle_info_level" IS '信息级别，标识不同级别的过车信息，1普通车辆，2红名单特权车辆，3红名单特殊车辆';
COMMENT ON COLUMN "postgres"."traffic_vehicle_pass"."vehicle_logo" IS '车辆品牌索引';
COMMENT ON COLUMN "postgres"."traffic_vehicle_pass"."vehicle_sublogo" IS '车辆子品牌索引';
COMMENT ON COLUMN "postgres"."traffic_vehicle_pass"."vehicle_model" IS '车辆年款索引';
COMMENT ON COLUMN "postgres"."traffic_vehicle_pass"."pilotsunvisor" IS '0-未知,1-打开遮阳板';

-- ----------------------------
-- Alter Sequences Owned By 
-- ----------------------------

-- ----------------------------
-- Indexes structure for table traffic_vehicle_pass
-- ----------------------------
CREATE INDEX "idx_vehiclepass_com2" ON "postgres"."traffic_vehicle_pass" USING btree ("pass_time", "crossing_id");
CREATE INDEX "idx_vehiclepass_com3" ON "postgres"."traffic_vehicle_pass" USING btree ("plate_no", "pass_time", "crossing_id");

-- ----------------------------
-- Triggers structure for table traffic_vehicle_pass
-- ----------------------------
CREATE TRIGGER "insert_traffic_vehicle_pass_trigger" BEFORE INSERT ON "postgres"."traffic_vehicle_pass"
FOR EACH ROW
EXECUTE PROCEDURE "traffic_vehicle_pass_insert_trigger"();

-- ----------------------------
-- Primary Key structure for table traffic_vehicle_pass
-- ----------------------------
ALTER TABLE "postgres"."traffic_vehicle_pass" ADD PRIMARY KEY ("pass_id");
