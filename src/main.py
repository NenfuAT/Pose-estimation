import pandas as pd
import numpy as np
from scipy.spatial.transform import Rotation as R
from vpython import *

# CSVからデータを読み込む
# CSVファイルには "time", "ω_x", "ω_y", "ω_z" の列があると想定
data = pd.read_csv("src/data/kisu_sebiraki_gyro.csv")

# 時間の列を取得
time_data_msec = data["time"].to_numpy()  # ミリ秒単位
time_data_sec = time_data_msec / 1000  # 秒単位に変換
# 角速度のデータを取得
gyro_data = data[["x", "y", "z"]].to_numpy()

# 3Dシーンのセットアップ
scene = canvas(title='3D Rotation Example', width=800, height=600)

# 3Dオブジェクトの作成
coin = cylinder(pos=vector(0, 0, 0), axis=vector(1, 0, 0), radius=2, length=0.02, color=color.yellow)
# 赤いディスクを追加、円柱の端から少しだけ突き出すように配置
# 長さ0.01のディスクを円柱の端より前に配置する
front_face = cylinder(pos=coin.pos+ coin.axis * (coin.length / 2), axis=vector(1, 0, 0), radius=1, length=0.04, color=color.red)
# 軸を示す矢印を追加
arrow_length = 4  # 矢印の長さ
x_arrow = arrow(pos=coin.pos, axis=vector(arrow_length, 0, 0), color=color.red, shaftwidth=0.1)
y_arrow = arrow(pos=coin.pos, axis=vector(0, arrow_length, 0), color=color.green, shaftwidth=0.1)
z_arrow = arrow(pos=coin.pos, axis=vector(0, 0, arrow_length), color=color.blue, shaftwidth=0.1)

# 初期四元数
q = R.from_quat([0, 0, 0, 1])

# シミュレーションのフレームループ
for i in range(1, len(time_data_sec)):
    # 時間ステップを計算
    delta_t = time_data_sec[i] - time_data_sec[i - 1]
    
    # 現在の角速度を取得
    current_gyro = gyro_data[i]
    
    # 角度変化を計算
    angle_change = current_gyro * delta_t
    
    # 角度変化を四元数で表現
    rotation = R.from_rotvec(angle_change)  # 回転ベクトルとして表現
    
    # 四元数を使ってオブジェクトを回転
    q = q * rotation  # 新しい四元数
    
    # 四元数を回転行列として使用
    rotation_matrix = q.as_matrix()  # 回転行列を取得
    
    # オブジェクトの新しい向きを設定
    coin.axis = vector(*rotation_matrix[:, 0]) * coin.length # 回転行列の1列目を使って軸を設定
    front_face.axis = vector(*rotation_matrix[:, 0]) * front_face.length # 回転行列の1列目を使って軸を設定
    # x_arrow.axis = vector(*rotation_matrix[:, 0]) * arrow_length
    # y_arrow.axis = vector(*rotation_matrix[:, 1]) * arrow_length
    # z_arrow.axis = vector(*rotation_matrix[:, 2]) * arrow_length
    # シミュレーションのスピードを設定
    rate(60)  # フレームレートを設定
