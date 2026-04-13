from launch import LaunchDescription
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from moveit_configs_utils import MoveItConfigsBuilder


def generate_launch_description():
    moveit_config = MoveItConfigsBuilder(
        "so101_new_calib",
        package_name="so_arm_moveit_config",
    ).to_moveit_configs()

    warehouse_ros_config = {
        "warehouse_plugin": "warehouse_ros_sqlite::DatabaseConnection",
        "warehouse_host": "/tmp/so101_moveit_warehouse.sqlite",
    }

    move_group_configuration = {
        "publish_robot_description_semantic": True,
        "allow_trajectory_execution": True,
        "capabilities": ParameterValue(
            moveit_config.move_group_capabilities["capabilities"], value_type=str
        ),
        "disable_capabilities": ParameterValue(
            moveit_config.move_group_capabilities["disable_capabilities"], value_type=str
        ),
        "publish_planning_scene": True,
        "publish_geometry_updates": True,
        "publish_state_updates": True,
        "publish_transforms_updates": True,
        "monitor_dynamics": False,
    }

    return LaunchDescription([
        Node(
            package="moveit_ros_move_group",
            executable="move_group",
            output="screen",
            parameters=[
                moveit_config.to_dict(),
                move_group_configuration,
                warehouse_ros_config,
            ],
        )
    ])