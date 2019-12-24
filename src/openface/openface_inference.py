#!usr/bin/env python3
# -*- coding:utf-8 _*-
'''
Copyright 2018 Soyoung All Rights Reserved.
@author:zqj
@file: openface_inference
@time: 7/18/19  3:07 PM
'''
import os
import sys
import numpy as np
import time
import warnings

warnings.filterwarnings("ignore")
import base64
import pandas as pd

kpoint_xcolumns = [" x_" + str(i) for i in range(68)]
kpoint_ycolumns = [" y_" + str(i) for i in range(68)]
kpoint_columns = kpoint_xcolumns + kpoint_ycolumns

kpoint_3dxcolumns = [" X_" + str(i) for i in range(68)]
kpoint_3dycolumns = [" Y_" + str(i) for i in range(68)]
kpoint_3dzcolumns = [" Z_" + str(i) for i in range(68)]
kpoint_3dcolumns = kpoint_3dxcolumns + kpoint_3dycolumns + kpoint_3dzcolumns
columns_name = ['face', ' confidence', ' gaze_0_x', ' gaze_0_y', ' gaze_0_z', ' gaze_1_x', ' gaze_1_y', ' gaze_1_z',
                ' gaze_angle_x', ' gaze_angle_y', ' eye_lmk_x_0', ' eye_lmk_x_1', ' eye_lmk_x_2', ' eye_lmk_x_3',
                ' eye_lmk_x_4', ' eye_lmk_x_5', ' eye_lmk_x_6', ' eye_lmk_x_7', ' eye_lmk_x_8', ' eye_lmk_x_9',
                ' eye_lmk_x_10', ' eye_lmk_x_11', ' eye_lmk_x_12', ' eye_lmk_x_13', ' eye_lmk_x_14', ' eye_lmk_x_15',
                ' eye_lmk_x_16', ' eye_lmk_x_17', ' eye_lmk_x_18', ' eye_lmk_x_19', ' eye_lmk_x_20', ' eye_lmk_x_21',
                ' eye_lmk_x_22', ' eye_lmk_x_23', ' eye_lmk_x_24', ' eye_lmk_x_25', ' eye_lmk_x_26', ' eye_lmk_x_27',
                ' eye_lmk_x_28', ' eye_lmk_x_29', ' eye_lmk_x_30', ' eye_lmk_x_31', ' eye_lmk_x_32', ' eye_lmk_x_33',
                ' eye_lmk_x_34', ' eye_lmk_x_35', ' eye_lmk_x_36', ' eye_lmk_x_37', ' eye_lmk_x_38', ' eye_lmk_x_39',
                ' eye_lmk_x_40', ' eye_lmk_x_41', ' eye_lmk_x_42', ' eye_lmk_x_43', ' eye_lmk_x_44', ' eye_lmk_x_45',
                ' eye_lmk_x_46', ' eye_lmk_x_47', ' eye_lmk_x_48', ' eye_lmk_x_49', ' eye_lmk_x_50', ' eye_lmk_x_51',
                ' eye_lmk_x_52', ' eye_lmk_x_53', ' eye_lmk_x_54', ' eye_lmk_x_55', ' eye_lmk_y_0', ' eye_lmk_y_1',
                ' eye_lmk_y_2', ' eye_lmk_y_3', ' eye_lmk_y_4', ' eye_lmk_y_5', ' eye_lmk_y_6', ' eye_lmk_y_7',
                ' eye_lmk_y_8', ' eye_lmk_y_9', ' eye_lmk_y_10', ' eye_lmk_y_11', ' eye_lmk_y_12', ' eye_lmk_y_13',
                ' eye_lmk_y_14', ' eye_lmk_y_15', ' eye_lmk_y_16', ' eye_lmk_y_17', ' eye_lmk_y_18', ' eye_lmk_y_19',
                ' eye_lmk_y_20', ' eye_lmk_y_21', ' eye_lmk_y_22', ' eye_lmk_y_23', ' eye_lmk_y_24', ' eye_lmk_y_25',
                ' eye_lmk_y_26', ' eye_lmk_y_27', ' eye_lmk_y_28', ' eye_lmk_y_29', ' eye_lmk_y_30', ' eye_lmk_y_31',
                ' eye_lmk_y_32', ' eye_lmk_y_33', ' eye_lmk_y_34', ' eye_lmk_y_35', ' eye_lmk_y_36', ' eye_lmk_y_37',
                ' eye_lmk_y_38', ' eye_lmk_y_39', ' eye_lmk_y_40', ' eye_lmk_y_41', ' eye_lmk_y_42', ' eye_lmk_y_43',
                ' eye_lmk_y_44', ' eye_lmk_y_45', ' eye_lmk_y_46', ' eye_lmk_y_47', ' eye_lmk_y_48', ' eye_lmk_y_49',
                ' eye_lmk_y_50', ' eye_lmk_y_51', ' eye_lmk_y_52', ' eye_lmk_y_53', ' eye_lmk_y_54', ' eye_lmk_y_55',
                ' eye_lmk_X_0', ' eye_lmk_X_1', ' eye_lmk_X_2', ' eye_lmk_X_3', ' eye_lmk_X_4', ' eye_lmk_X_5',
                ' eye_lmk_X_6', ' eye_lmk_X_7', ' eye_lmk_X_8', ' eye_lmk_X_9', ' eye_lmk_X_10', ' eye_lmk_X_11',
                ' eye_lmk_X_12', ' eye_lmk_X_13', ' eye_lmk_X_14', ' eye_lmk_X_15', ' eye_lmk_X_16', ' eye_lmk_X_17',
                ' eye_lmk_X_18', ' eye_lmk_X_19', ' eye_lmk_X_20', ' eye_lmk_X_21', ' eye_lmk_X_22', ' eye_lmk_X_23',
                ' eye_lmk_X_24', ' eye_lmk_X_25', ' eye_lmk_X_26', ' eye_lmk_X_27', ' eye_lmk_X_28', ' eye_lmk_X_29',
                ' eye_lmk_X_30', ' eye_lmk_X_31', ' eye_lmk_X_32', ' eye_lmk_X_33', ' eye_lmk_X_34', ' eye_lmk_X_35',
                ' eye_lmk_X_36', ' eye_lmk_X_37', ' eye_lmk_X_38', ' eye_lmk_X_39', ' eye_lmk_X_40', ' eye_lmk_X_41',
                ' eye_lmk_X_42', ' eye_lmk_X_43', ' eye_lmk_X_44', ' eye_lmk_X_45', ' eye_lmk_X_46', ' eye_lmk_X_47',
                ' eye_lmk_X_48', ' eye_lmk_X_49', ' eye_lmk_X_50', ' eye_lmk_X_51', ' eye_lmk_X_52', ' eye_lmk_X_53',
                ' eye_lmk_X_54', ' eye_lmk_X_55', ' eye_lmk_Y_0', ' eye_lmk_Y_1', ' eye_lmk_Y_2', ' eye_lmk_Y_3',
                ' eye_lmk_Y_4', ' eye_lmk_Y_5', ' eye_lmk_Y_6', ' eye_lmk_Y_7', ' eye_lmk_Y_8', ' eye_lmk_Y_9',
                ' eye_lmk_Y_10', ' eye_lmk_Y_11', ' eye_lmk_Y_12', ' eye_lmk_Y_13', ' eye_lmk_Y_14', ' eye_lmk_Y_15',
                ' eye_lmk_Y_16', ' eye_lmk_Y_17', ' eye_lmk_Y_18', ' eye_lmk_Y_19', ' eye_lmk_Y_20', ' eye_lmk_Y_21',
                ' eye_lmk_Y_22', ' eye_lmk_Y_23', ' eye_lmk_Y_24', ' eye_lmk_Y_25', ' eye_lmk_Y_26', ' eye_lmk_Y_27',
                ' eye_lmk_Y_28', ' eye_lmk_Y_29', ' eye_lmk_Y_30', ' eye_lmk_Y_31', ' eye_lmk_Y_32', ' eye_lmk_Y_33',
                ' eye_lmk_Y_34', ' eye_lmk_Y_35', ' eye_lmk_Y_36', ' eye_lmk_Y_37', ' eye_lmk_Y_38', ' eye_lmk_Y_39',
                ' eye_lmk_Y_40', ' eye_lmk_Y_41', ' eye_lmk_Y_42', ' eye_lmk_Y_43', ' eye_lmk_Y_44', ' eye_lmk_Y_45',
                ' eye_lmk_Y_46', ' eye_lmk_Y_47', ' eye_lmk_Y_48', ' eye_lmk_Y_49', ' eye_lmk_Y_50', ' eye_lmk_Y_51',
                ' eye_lmk_Y_52', ' eye_lmk_Y_53', ' eye_lmk_Y_54', ' eye_lmk_Y_55', ' eye_lmk_Z_0', ' eye_lmk_Z_1',
                ' eye_lmk_Z_2', ' eye_lmk_Z_3', ' eye_lmk_Z_4', ' eye_lmk_Z_5', ' eye_lmk_Z_6', ' eye_lmk_Z_7',
                ' eye_lmk_Z_8', ' eye_lmk_Z_9', ' eye_lmk_Z_10', ' eye_lmk_Z_11', ' eye_lmk_Z_12', ' eye_lmk_Z_13',
                ' eye_lmk_Z_14', ' eye_lmk_Z_15', ' eye_lmk_Z_16', ' eye_lmk_Z_17', ' eye_lmk_Z_18', ' eye_lmk_Z_19',
                ' eye_lmk_Z_20', ' eye_lmk_Z_21', ' eye_lmk_Z_22', ' eye_lmk_Z_23', ' eye_lmk_Z_24', ' eye_lmk_Z_25',
                ' eye_lmk_Z_26', ' eye_lmk_Z_27', ' eye_lmk_Z_28', ' eye_lmk_Z_29', ' eye_lmk_Z_30', ' eye_lmk_Z_31',
                ' eye_lmk_Z_32', ' eye_lmk_Z_33', ' eye_lmk_Z_34', ' eye_lmk_Z_35', ' eye_lmk_Z_36', ' eye_lmk_Z_37',
                ' eye_lmk_Z_38', ' eye_lmk_Z_39', ' eye_lmk_Z_40', ' eye_lmk_Z_41', ' eye_lmk_Z_42', ' eye_lmk_Z_43',
                ' eye_lmk_Z_44', ' eye_lmk_Z_45', ' eye_lmk_Z_46', ' eye_lmk_Z_47', ' eye_lmk_Z_48', ' eye_lmk_Z_49',
                ' eye_lmk_Z_50', ' eye_lmk_Z_51', ' eye_lmk_Z_52', ' eye_lmk_Z_53', ' eye_lmk_Z_54', ' eye_lmk_Z_55',
                ' pose_Tx', ' pose_Ty', ' pose_Tz', ' pose_Rx', ' pose_Ry', ' pose_Rz', ' x_0', ' x_1', ' x_2', ' x_3',
                ' x_4', ' x_5', ' x_6', ' x_7', ' x_8', ' x_9', ' x_10', ' x_11', ' x_12', ' x_13', ' x_14', ' x_15',
                ' x_16', ' x_17', ' x_18', ' x_19', ' x_20', ' x_21', ' x_22', ' x_23', ' x_24', ' x_25', ' x_26',
                ' x_27', ' x_28', ' x_29', ' x_30', ' x_31', ' x_32', ' x_33', ' x_34', ' x_35', ' x_36', ' x_37',
                ' x_38', ' x_39', ' x_40', ' x_41', ' x_42', ' x_43', ' x_44', ' x_45', ' x_46', ' x_47', ' x_48',
                ' x_49', ' x_50', ' x_51', ' x_52', ' x_53', ' x_54', ' x_55', ' x_56', ' x_57', ' x_58', ' x_59',
                ' x_60', ' x_61', ' x_62', ' x_63', ' x_64', ' x_65', ' x_66', ' x_67', ' y_0', ' y_1', ' y_2', ' y_3',
                ' y_4', ' y_5', ' y_6', ' y_7', ' y_8', ' y_9', ' y_10', ' y_11', ' y_12', ' y_13', ' y_14', ' y_15',
                ' y_16', ' y_17', ' y_18', ' y_19', ' y_20', ' y_21', ' y_22', ' y_23', ' y_24', ' y_25', ' y_26',
                ' y_27', ' y_28', ' y_29', ' y_30', ' y_31', ' y_32', ' y_33', ' y_34', ' y_35', ' y_36', ' y_37',
                ' y_38', ' y_39', ' y_40', ' y_41', ' y_42', ' y_43', ' y_44', ' y_45', ' y_46', ' y_47', ' y_48',
                ' y_49', ' y_50', ' y_51', ' y_52', ' y_53', ' y_54', ' y_55', ' y_56', ' y_57', ' y_58', ' y_59',
                ' y_60', ' y_61', ' y_62', ' y_63', ' y_64', ' y_65', ' y_66', ' y_67', ' X_0', ' X_1', ' X_2', ' X_3',
                ' X_4', ' X_5', ' X_6', ' X_7', ' X_8', ' X_9', ' X_10', ' X_11', ' X_12', ' X_13', ' X_14', ' X_15',
                ' X_16', ' X_17', ' X_18', ' X_19', ' X_20', ' X_21', ' X_22', ' X_23', ' X_24', ' X_25', ' X_26',
                ' X_27', ' X_28', ' X_29', ' X_30', ' X_31', ' X_32', ' X_33', ' X_34', ' X_35', ' X_36', ' X_37',
                ' X_38', ' X_39', ' X_40', ' X_41', ' X_42', ' X_43', ' X_44', ' X_45', ' X_46', ' X_47', ' X_48',
                ' X_49', ' X_50', ' X_51', ' X_52', ' X_53', ' X_54', ' X_55', ' X_56', ' X_57', ' X_58', ' X_59',
                ' X_60', ' X_61', ' X_62', ' X_63', ' X_64', ' X_65', ' X_66', ' X_67', ' Y_0', ' Y_1', ' Y_2', ' Y_3',
                ' Y_4', ' Y_5', ' Y_6', ' Y_7', ' Y_8', ' Y_9', ' Y_10', ' Y_11', ' Y_12', ' Y_13', ' Y_14', ' Y_15',
                ' Y_16', ' Y_17', ' Y_18', ' Y_19', ' Y_20', ' Y_21', ' Y_22', ' Y_23', ' Y_24', ' Y_25', ' Y_26',
                ' Y_27', ' Y_28', ' Y_29', ' Y_30', ' Y_31', ' Y_32', ' Y_33', ' Y_34', ' Y_35', ' Y_36', ' Y_37',
                ' Y_38', ' Y_39', ' Y_40', ' Y_41', ' Y_42', ' Y_43', ' Y_44', ' Y_45', ' Y_46', ' Y_47', ' Y_48',
                ' Y_49', ' Y_50', ' Y_51', ' Y_52', ' Y_53', ' Y_54', ' Y_55', ' Y_56', ' Y_57', ' Y_58', ' Y_59',
                ' Y_60', ' Y_61', ' Y_62', ' Y_63', ' Y_64', ' Y_65', ' Y_66', ' Y_67', ' Z_0', ' Z_1', ' Z_2', ' Z_3',
                ' Z_4', ' Z_5', ' Z_6', ' Z_7', ' Z_8', ' Z_9', ' Z_10', ' Z_11', ' Z_12', ' Z_13', ' Z_14', ' Z_15',
                ' Z_16', ' Z_17', ' Z_18', ' Z_19', ' Z_20', ' Z_21', ' Z_22', ' Z_23', ' Z_24', ' Z_25', ' Z_26',
                ' Z_27', ' Z_28', ' Z_29', ' Z_30', ' Z_31', ' Z_32', ' Z_33', ' Z_34', ' Z_35', ' Z_36', ' Z_37',
                ' Z_38', ' Z_39', ' Z_40', ' Z_41', ' Z_42', ' Z_43', ' Z_44', ' Z_45', ' Z_46', ' Z_47', ' Z_48',
                ' Z_49', ' Z_50', ' Z_51', ' Z_52', ' Z_53', ' Z_54', ' Z_55', ' Z_56', ' Z_57', ' Z_58', ' Z_59',
                ' Z_60', ' Z_61', ' Z_62', ' Z_63', ' Z_64', ' Z_65', ' Z_66', ' Z_67', ' p_scale', ' p_rx', ' p_ry',
                ' p_rz', ' p_tx', ' p_ty', ' p_0', ' p_1', ' p_2', ' p_3', ' p_4', ' p_5', ' p_6', ' p_7', ' p_8',
                ' p_9', ' p_10', ' p_11', ' p_12', ' p_13', ' p_14', ' p_15', ' p_16', ' p_17', ' p_18', ' p_19',
                ' p_20', ' p_21', ' p_22', ' p_23', ' p_24', ' p_25', ' p_26', ' p_27', ' p_28', ' p_29', ' p_30',
                ' p_31', ' p_32', ' p_33', ' AU01_r', ' AU02_r', ' AU04_r', ' AU05_r', ' AU06_r', ' AU07_r', ' AU09_r',
                ' AU10_r', ' AU12_r', ' AU14_r', ' AU15_r', ' AU17_r', ' AU20_r', ' AU23_r', ' AU25_r', ' AU26_r',
                ' AU45_r', ' AU01_c', ' AU02_c', ' AU04_c', ' AU05_c', ' AU06_c', ' AU07_c', ' AU09_c', ' AU10_c',
                ' AU12_c', ' AU14_c', ' AU15_c', ' AU17_c', ' AU20_c', ' AU23_c', ' AU25_c', ' AU26_c', ' AU28_c',
                ' AU45_c']
gaze_c = columns_name[2:8]
gazeangel_c = columns_name[8:10]
eye_lmk_c = columns_name[10:122]
eye3dlmk_c = columns_name[122:290]
pose_c = columns_name[290:296]
pscale_c = columns_name[636]
pr_c = columns_name[637:640]
pt_c = columns_name[640:642]
p_c = columns_name[642:676]
AU_c = columns_name[676:]



def openface_inference(bn):
    # bn = os.path.splitext(filename)[0]
    # if not os.path.exists(os.path.join("static/tmp", bn)):
    #     cmd = "docker exec  openface FaceLandmarkImg -f /tmp/" + filename + "  -out_dir /tmp/" + bn + " -nomask"
    #     os.system(cmd)
    with open(os.path.join("static/tmpimg/", bn, bn + "_openface.jpg"), "rb") as f:
        file_binary = f.read()
    b64img = 'data:image/jpeg;base64,' + base64.b64encode(file_binary).decode()
    df = pd.read_csv(os.path.join("static/tmpimg/", bn, bn + "_openface.csv"))
    kpointx = df.loc[:, kpoint_xcolumns].values
    kpointy = df.loc[:, kpoint_ycolumns].values
    kpoint = np.concatenate([kpointx, kpointy], axis=1)
    xmin, xmax = np.expand_dims(np.min(kpointx, axis=1), 1), np.expand_dims(np.max(kpointx, axis=1), 1)
    ymin, ymax = np.expand_dims(np.min(kpointy, axis=1), 1), np.expand_dims(np.max(kpointy, axis=1), 1)
    bounding_boxes = np.concatenate([xmin, ymin, xmax, ymax], axis=1)
    confidence = df.loc[:, " confidence"].values
    face_count = len(bounding_boxes)
    face_res = []
    kpoint3d = df.loc[:,kpoint_3dcolumns]
    gaze = df.loc[:, gaze_c]
    gazeangel = df.loc[:, gazeangel_c]
    eye_lmk = df.loc[:, eye_lmk_c]
    eye3dlmk = df.loc[:, eye3dlmk_c]
    pose = df.loc[:, pose_c]
    pscale = df.loc[:, pscale_c]
    pr = df.loc[:, pr_c]
    pt = df.loc[:, pt_c]
    p = df.loc[:, p_c]
    AU = df.loc[:, AU_c]
    for i in range(face_count):
        res = {"bounding_boxes": {"x1": int(bounding_boxes[i, 0]), "y1": int(bounding_boxes[i, 1]),
                                  "x2": int(bounding_boxes[i, 2]), "y2": int(bounding_boxes[i, 3])},
               "confidence": "%.3f" % confidence[i],
               "kpoint": np.reshape(kpoint[i], (2, 68)).transpose((1, 0)).astype(np.int).tolist(),
               "kpoint3D": kpoint3d.loc[i, :].to_dict(),
               "gaze": gaze.loc[i, :].to_dict(),
               "gazeangel": gazeangel.loc[i, :].to_dict(),
               "eye_lmk": eye_lmk.loc[i, :].to_dict(),
               "eye3dlmk": eye3dlmk.loc[i, :].to_dict(),
               "pose": pose.loc[i, :].to_dict(),
               "pscale": pscale.loc[i],
               "pr": pr.loc[i, :].to_dict(),
               "pt": pt.loc[i, :].to_dict(),
               "p": p.loc[i, :].to_dict(),
               "AU": AU.loc[i, :].to_dict(),
               }
        face_res.append(res)
    result = {"faces": face_res, "b64_img": b64img}
    return result


if __name__ == '__main__':
    pass
