from robovac import Robovac

my_robovac = Robovac('192.168.0.55', 'b9eb4c848f02c1df')

# Cleaning modes
my_robovac.start_auto_clean()
# my_robovac.start_edge_clean()
# my_robovac.start_single_room_clean()
# my_robovac.start_spot_clean()

# # Set cleaning speed
# my_robovac.use_normal_speed()
# my_robovac.use_max_speed()

# # Stop cleaning
# my_robovac.stop()

# # Return to charging base
# my_robovac.go_home()

# # Activate "find me" mode, plays a tone until deactivated
# my_robovac.start_find_me()
# my_robovac.stop_find_me()

# # Move in a given direction
# my_robovac.go_forward()
# my_robovac.go_backward()
# my_robovac.go_left()
# my_robovac.go_right()

# # Get RoboVac status
# my_robovac.get_status()