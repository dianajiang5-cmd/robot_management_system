from datetime import datetime
from sqlalchemy import String,Integer,Float,Boolean,DateTime,Date,ForeignKey,Text,Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship,Mapped,mapped_column
import enum


#这里创建的模型类都会在数据库里形成数据结构来存储数据
Base=declarative_base()

#用户权限
class UserRole(str,enum.Enum):
    ADMIN='admin'#管理员，全部权限
    EDITOR='editor'#维护人员，可以处理警告，填写维修记录
    VIEWER='viewer' #只能读和看，不能修改，适用工人

#告警级别
class AlertLevel(str,enum.Enum):
    INFO='info'
    WARNING='warning'#警告
    ERROR='error'#错误
    CRITICAL='critical'#严重
#机器人状态
class RobotStatus(str,enum.Enum):
    ONLINE='online'#在线
    OFFLINE='offline'#不在线
    FAULT='fault'#故障
    MAINTENANCE='maintenance'#维修

#用户模型类
class User(Base):
    __tablename__ ='user'
    id:Mapped[int]=mapped_column(Integer,primary_key=True,autoincrement=True,comment='id')
    username:Mapped[str]=mapped_column(String(50),unique=True,index=True,nullable=False,comment='username')
    email:Mapped[str]=mapped_column(String(100),unique=True,index=True,comment='email')
    hashed_password:Mapped[str]=mapped_column(String(100),nullable=False)#bcrypt加密后的密码，不存明文
    role_name:Mapped[UserRole]=mapped_column(Enum(UserRole),default=UserRole.VIEWER,comment='role_name')
    is_active:Mapped[bool]=mapped_column(Boolean,default=True,comment='status')
    created_at:Mapped[datetime]=mapped_column(DateTime,default=datetime.now,comment='creat_time')
    updated_at:Mapped[datetime]=mapped_column(DateTime,default=datetime.now,comment='update_time')

    maintenance_records = relationship("MaintenanceRecord", back_populates="user")
    resolved_alerts = relationship("Alert", back_populates="resolver")


#站点模型类
class Site(Base):
    __tablename__ ='site'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, comment='站点id')
    site_name:Mapped[str]=mapped_column(String(50),nullable=False,index=True,comment='站点名称')
    location:Mapped[str]=mapped_column(String,nullable=True,comment='站点位置')
    is_active:Mapped[bool]=mapped_column(Boolean,default=True,comment='是否启用')
    created_at:Mapped[datetime]=mapped_column(DateTime,default=datetime.now,comment='update_at')
    updated_at:Mapped[datetime]=mapped_column(DateTime,default=datetime.now,onupdate=datetime.now,comment='update_at')

    robots = relationship("Robot", back_populates="site", cascade="all, delete-orphan")


#机器人模型类
class Robot(Base):
    __tablename__ ='robot'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment='id')
    name: Mapped[str] = mapped_column(String(50), unique=True,nullable=False,comment='Robot_name')
    status: Mapped[str] = mapped_column(String(20),default="idle",comment='Robot_status:idle空闲,working工作中,offline离线')
    robot_type: Mapped[str] = mapped_column(String(20),nullable=False,comment='Robot_type:delivery,cleaning')
    created_by:Mapped[str]=mapped_column(String(20),nullable=True,comment='创建人')
    #外键关联到站点
    site_id:Mapped[int]=mapped_column(Integer,ForeignKey('site.id'),nullable=False,comment='site_id')

    ip_address:Mapped[str]=mapped_column(String(50),nullable=True,comment='ip地址')

    purchase_date:Mapped[Date]=mapped_column(Date,comment='购买日期')
    warranty_end_date:Mapped[Date]=mapped_column(Date,comment='保修期')
    created_at:Mapped[DateTime]=mapped_column(DateTime,default=datetime.now,comment='创建日期')

    site=relationship('Site',back_populates='robots')
    parameters=relationship('RobotParameter',back_populates='robot',cascade="all, delete-orphan")
    alerts=relationship('Alert',back_populates='robot', cascade="all, delete-orphan")
    maintenance_records = relationship("MaintenanceRecord", back_populates="robot")


#机器人参数模型类
class RobotParameter(Base):
    __tablename__ ='robot_parameters'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment='id')
    robot_id:Mapped[int]=mapped_column(Integer,ForeignKey('robot.id'),nullable=False,comment='机器人id')

    name:Mapped[str]=mapped_column(String(80),nullable=False,comment='参数名称')#参数名：温度，电压等
    value:Mapped[int]=mapped_column(Float,nullable=False,comment='当前数值')
    unit:Mapped[int]=mapped_column(String(20),comment='数值单位')#C,V,A
    min_threshold:Mapped[int]=mapped_column(Float,comment='threshold_min')#阈值下限
    max_threshold:Mapped[int]=mapped_column(Float,comment='threshold_max')#阈值上限
    is_abnormal:Mapped[bool]=mapped_column(Boolean,default=False,comment='is_abnormal')#超出阈值自动标记异常
    report_time:Mapped[datetime]=mapped_column(DateTime,default=datetime.now,comment='上报时间')
    created_at:Mapped[datetime]=mapped_column(DateTime,default=datetime.now)

    robot=relationship('Robot',back_populates='parameters')


#警报模型类
class Alert(Base):
    __tablename__ ='alerts'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment='id')
    robot_id:Mapped[int]=mapped_column(Integer,ForeignKey('robot.id'),nullable=False,comment='robot_id')

    message: Mapped[str] = mapped_column(String(200), nullable=False, comment='告警信息')

    level:Mapped[str]=mapped_column(String(20),default='warning' )
    is_resolved:Mapped[bool]=mapped_column(Boolean,default=False,comment='是否已经解决警报')

    resolver_id:Mapped[int|None]=mapped_column(Integer,ForeignKey('user.id'),nullable=True,comment='处理人')
    resolve_note:Mapped[str|None]=mapped_column(String(200),nullable=True,comment='处理警报备注内容')

    resolved_date: Mapped[datetime|None] = mapped_column(DateTime, default=None,nullable=True,comment='处理日期')
    created_at:Mapped[datetime]=mapped_column(DateTime,default=datetime.now,comment='告警日期')

    robot=relationship('Robot',back_populates='alerts')
    resolver = relationship("User", back_populates="resolved_alerts")


#维修记录模型类
class MaintenanceRecord(Base):
    __tablename__ ='maintenance_records'
    id:Mapped[int]=mapped_column(Integer,primary_key=True, autoincrement=True, comment='维修id')
    robot_id:Mapped[int]=mapped_column(Integer,ForeignKey('robot.id'),nullable=False,comment='robot_id')
    maintain_type: Mapped[str] = mapped_column(String(20), comment='维修类型:日常，故障，升级')
    description: Mapped[str] = mapped_column(String(200), comment='维修内容描述')
    cost: Mapped[float] = mapped_column(Float, default=0, comment='维修费用')
    duration:Mapped[int]=mapped_column(Integer,default=0,comment='耗时')
    performer_id:Mapped[int]=mapped_column(Integer,ForeignKey('user.id'),comment='维修人员ID')
    created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    user = relationship("User", back_populates="maintenance_records")
    robot = relationship("Robot", back_populates="maintenance_records")










