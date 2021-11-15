import pandas as pd
import math

# 二维超声风文件
wind_2d_file = '../data/WindSonic_2D/TOA5_2016_06_01_0000.dat'
# 近地层观测数据集文件
near_surface_file = '../data/10min/TOA5__2016_06_01_0010.dat'
# 风廓线雷达文件

# 微波辐射计文件

alt = 86#HCEO 海拔高度

###HCEO二维超声风观察数据 --> u,v —————— 指定时间索引和高度
def GetUV(file, t_id, z):
    u = []
    v = []
    df = pd.read_csv(file)
    for i in z:
        name = 'U_' + str(i) + 'M'
        if i == 35:
            name += '_1'
        u.append(df[name][t_id])
        name = 'V_' + str(i) + 'M'
        if i == 35:
            name += '_1'
        v.append(df[name][t_id])
    print('WindSonic2D date_time:', df['Year'][t_id], df['Month'][t_id], df['Day'][t_id], df['Hour'][t_id],
          df['Minute'][t_id], df['Second'][t_id])
    return u,v
###HCEO近底层气象观察数据 --> theta,qv,t_2,q_2,psfc ————————————z高度，sz土壤深度
def Getthetaqv(file, t_id, z, sz):
    theta = []
    qv = []
    SOILT = []
    df = pd.read_csv(file)
    for i in z:
        ####绝对温度，气压计算位温
        name = 'Ta_' + str(i) + 'M_Avg'
        ta = df[name][t_id]
        name = 'e_' + str(i) + 'M_Avg'
        pa = (alt + i) / 9. + 1013.25
        theta.append((ta + 273.16) * math.pow(1000 / pa, 0.286))
        ####相对湿度计算比湿
        name = 'RH_' + str(i) + 'M_Avg'
        rha = df[name][t_id] * 0.01
        es = 6.112 * math.exp((17.67 * ta) / (ta + 243.5))
        e = rha * es
        qv.append((0.622 * e) / (pa - (0.378 * e)))
    for i in sz:
        name = 'T_Soil_' + format(i * 100, '.0f') + 'CM_Avg'
        SOILT.append(df[name][t_id] + 273.15)
    print('Near-bottom meteorological observation data date_time:', df['Year'][t_id], df['Month'][t_id],
          df['Day'][t_id], df['Hour'][t_id],
          df['Minute'][t_id], df['Second'][t_id])
    return theta,qv,df['Ta_10M_Avg'][t_id],qv[0],SOILT
###风廓线雷达资料-->u, v (>100m)
def GetUVFromWindProfileRadar(file):

    return 0

#input_sounding
##地面高度，10米东西、南北风，2米温度、2米比湿、地面气压
z_terrian = 0
u_10 = 0
v_10 = 0
t_2 = 0
q_2 = 0
psfc = (alt / 9. + 1013.25) * 100
##高度，东西，南北风，位温，比湿
z = [10, 20, 35, 52, 70, 95]
u = []
v = []
theta = []
qv = []
#input_soil
##
TSK = t_2
TMN = t_2
sz = [0.1, 0.2]
SOILT = []
SOILM = [0.25, 0.25]

###数据获取
###HCEO二维超声风观察数据 --> z,u,v
u,v = GetUV('../data/WindSonic_2D/TOA5_2016_06_01_0000.dat', 599, z)#599
###HCEO近底层气象观察数据 --> theta,qv,t_2,q_2,psfc,SOILT
theta, qv, t_2, q_2, SOILT = Getthetaqv('../data/10min/TOA5__2016_06_01_0010.dat', 1, z, sz)#1
t_2 += 273.15
###地面数据
u_10 = u[0]
v_10 = v[0]
###Soil data
TSK = t_2
TMN = t_2

####输出input_sounding
with open("../doc/input_sounding","w") as f:
    f.write(format(z_terrian, '.1f') + ' ' + format(u_10, '.1f') + ' ' + format(v_10, '.1f')
            + ' ' + format(t_2, '.1f') + ' ' + format(q_2, '.4f')+ ' ' + format(psfc, '.1f'))
    f.write('\n')
    for i in range(len(z)):
        f.write(format(z[i], '.1f') + ' ' + format(u[i], '.1f') + ' ' + format(v[i], '.1f')
                + ' ' + format(theta[i], '.1f') + ' ' + format(qv[i], '.4f'))
        f.write('\n')
####输出input_soil
with open("../doc/input_soil","w") as f:
    f.write(format(0.0, '.7f') + ' ' + format(TSK, '.7f') + ' ' + format(TMN, '.7f'))
    f.write('\n')
    for i in range(len(sz)):
        f.write(format(sz[i], '.7f') + ' ' + format(SOILT[i], '.7f') + ' ' + format(SOILM[i], '.7f'))
        f.write('\n')

print('<<sounding>>')
print('z_terrian:', z_terrian)
print('u_10:', u_10)
print('v_10:', v_10)
print('t_2:', t_2)
print('q_2:', q_2)
print('psfc:', psfc)
print('z:', z)
print('u:', u)
print('v:', v)
print('theta:', theta)
print('qv:', qv)
print('<<soil>>')
print('0.0:', 0.0)
print('TSK:', TSK)
print('TMN', TMN)
print('sz:', sz)
print('SOILT:', SOILT)
print('SOILM:', SOILM)