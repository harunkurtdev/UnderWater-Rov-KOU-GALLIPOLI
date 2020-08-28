from pymavlink import mavutil

def arm_ardusub(master):
	master.mav.command_long_send(
		master.target_system,
		master.target_component,
		mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
		0,
		1, 0, 0, 0, 0, 0, 0)

def disarm_ardusub(master):
	master.mav.command_long_send(
		master.target_system,
		master.target_component,
		mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
		0,
		0, 0, 0, 0, 0, 0, 0)


master = mavutil.mavlink_connection('udpin:192.168.2.1:14550')
master.wait_heartbeat()
arm_ardusub(master)