/*
 Navicat Premium Data Transfer

 Source Server         : localhost_3306
 Source Server Type    : MySQL
 Source Server Version : 50736
 Source Host           : localhost:3306
 Source Schema         : python_shop

 Target Server Type    : MySQL
 Target Server Version : 50736
 File Encoding         : 65001

 Date: 28/12/2023 20:08:00
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for system_goods
-- ----------------------------
DROP TABLE IF EXISTS `system_goods`;
CREATE TABLE `system_goods`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '名称',
  `price` decimal(10, 2) NULL DEFAULT NULL COMMENT '单价',
  `store` int(10) NULL DEFAULT NULL COMMENT '库存',
  `unit` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '单位',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 16 CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of system_goods
-- ----------------------------
INSERT INTO `system_goods` VALUES (1, '月度会员', 5.00, 99999, '个');
INSERT INTO `system_goods` VALUES (2, '季度会员', 12.00, 99999, '个');
INSERT INTO `system_goods` VALUES (3, '年度会员', 42.01, 99999, '个');
INSERT INTO `system_goods` VALUES (4, '族谱定制', 4988.00, 99999, '50本');
INSERT INTO `system_goods` VALUES (13, '超级会员', 100.00, 99999, '1');

-- ----------------------------
-- Table structure for system_menu
-- ----------------------------
DROP TABLE IF EXISTS `system_menu`;
CREATE TABLE `system_menu`  (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'id',
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '名称',
  `path` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '路径',
  `icon` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '图标',
  `description` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '描述',
  `pid` int(11) NULL DEFAULT NULL COMMENT '父级id',
  `page_path` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '页面路径',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 11 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of system_menu
-- ----------------------------
INSERT INTO `system_menu` VALUES (1, '主页', '/home', 'el-icon-user', '', NULL, 'Home');
INSERT INTO `system_menu` VALUES (2, '系统管理', NULL, 'el-icon-s-grid', NULL, NULL, NULL);
INSERT INTO `system_menu` VALUES (3, '用户管理', '/user', 'el-icon-user', NULL, 2, 'User');
INSERT INTO `system_menu` VALUES (5, '商品管理', '/good', 'el-icon-goods', NULL, 2, 'Good');
INSERT INTO `system_menu` VALUES (6, '订单管理', '/order', 'el-icon-s-order', NULL, 2, 'Order');
INSERT INTO `system_menu` VALUES (7, '数据报表', '/dashbord', 'el-icon-s-marketing', NULL, NULL, 'Dashbord');
INSERT INTO `system_menu` VALUES (10, '地图', '/map', 'el-icon-s-grid', NULL, NULL, 'Map');

-- ----------------------------
-- Table structure for system_role
-- ----------------------------
DROP TABLE IF EXISTS `system_role`;
CREATE TABLE `system_role`  (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'id',
  `name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '名称',
  `description` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '描述',
  `flag` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '唯一标识',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of system_role
-- ----------------------------
INSERT INTO `system_role` VALUES (1, '管理员', '管理员', 'ROLE_ADMIN');
INSERT INTO `system_role` VALUES (2, '普通用户', '普通用户', 'ROLE_USER');

-- ----------------------------
-- Table structure for system_sales
-- ----------------------------
DROP TABLE IF EXISTS `system_sales`;
CREATE TABLE `system_sales`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `goods_id` int(11) NULL DEFAULT NULL COMMENT '商品编号',
  `user_id` int(11) NULL DEFAULT NULL COMMENT '用户id',
  `goods_num` int(11) NULL DEFAULT 1 COMMENT '商品数目',
  `time` timestamp(0) NULL DEFAULT CURRENT_TIMESTAMP(0) ON UPDATE CURRENT_TIMESTAMP(0),
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 15 CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of system_sales
-- ----------------------------
INSERT INTO `system_sales` VALUES (5, 13, 999, 65, '2023-12-27 22:41:45');
INSERT INTO `system_sales` VALUES (9, 1, 111, 12, '2023-12-28 08:49:39');
INSERT INTO `system_sales` VALUES (10, 9, 55, 1147, '2023-12-27 15:24:47');
INSERT INTO `system_sales` VALUES (11, 2, 55, 33, '2023-12-27 22:48:07');
INSERT INTO `system_sales` VALUES (12, 4, 114, 114, '2023-12-28 11:16:16');
INSERT INTO `system_sales` VALUES (13, 4, 114, 114, '2023-12-28 11:17:09');
INSERT INTO `system_sales` VALUES (14, 4, 57, 1, '2023-12-28 17:28:18');

-- ----------------------------
-- Table structure for system_user
-- ----------------------------
DROP TABLE IF EXISTS `system_user`;
CREATE TABLE `system_user`  (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'id',
  `username` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '用户名',
  `password` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT '123456' COMMENT '密码',
  `nickname` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '昵称',
  `address` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '地址',
  `create_time` timestamp(0) NULL DEFAULT CURRENT_TIMESTAMP(0) COMMENT '创建时间',
  `avatarUrl` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '头像',
  `role` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '角色',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 20 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of system_user
-- ----------------------------
INSERT INTO `system_user` VALUES (8, 'scarlet', 'admin', 'scarlet', '889', '2023-12-23 21:43:59', NULL, 'ROLE_ADMIN');
INSERT INTO `system_user` VALUES (11, 'iuy', '123456', 'iuy', 'fdsc45', '2023-12-24 10:10:11', 'https://img10.360buyimg.com/img/jfs/t1/192028/25/33459/5661/63fc2af2F1f6ae1b6/d0e4fdc2f126cbf5.png', 'ROLE_USER');
INSERT INTO `system_user` VALUES (12, 'admin', 'admin', 'administrat', '44587]]44', '2023-12-26 17:21:55', 'https://s1.ax1x.com/2022/12/05/zy6V4x.png', 'ROLE_ADMIN');
INSERT INTO `system_user` VALUES (13, 'yearn', '123456', NULL, NULL, '2023-12-27 08:58:21', NULL, 'ROLE_USER');
INSERT INTO `system_user` VALUES (14, 'zxc', '123456', 'zxc', NULL, '2023-12-27 09:01:03', 'https://wwc.alicdn.com/avatar/getAvatar.do?userNick=&width=60&height=60&type=sns&_input_charset=UTF-8', 'ROLE_USER');
INSERT INTO `system_user` VALUES (15, 'vbn', '123456', 'vbnn', '54658455', '2023-12-27 09:02:34', 'https://img14.360buyimg.com/imagetools/jfs/t1/66037/3/24346/9414/64b11b21F51d90361/8f015973cbb7de8d.png', 'ROLE_ADMIN');
INSERT INTO `system_user` VALUES (19, 'qwe', '123456', 'qwe', NULL, '2023-12-28 11:45:06', NULL, 'ROLE_USER');

SET FOREIGN_KEY_CHECKS = 1;
