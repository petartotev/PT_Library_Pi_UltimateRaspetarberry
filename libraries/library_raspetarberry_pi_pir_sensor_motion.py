from gpiozero import MotionSensor

pir = MotionSensor(4)

def UseMotionSensor():
    try:
        pir.wait_for_motion()
        # Do some business logic here.
        pir.wait_for_no_motion()
        # Do some other business logic here.
    except KeyboardInterrupt:
        # Handle KeyboardInterrupt.