import environment
import deepmind_lab
import cv2
import numpy as np


def _action(*entries):
  return np.array(entries, dtype=np.intc)


class LabEnvironment(environment.Environment):
  ACTIONS = {
      'look_left':    _action(-20,   0,  0,  0, 0, 0, 0),
      'look_right':   _action( 20,   0,  0,  0, 0, 0, 0),
      'look_up':      _action(  0,  10,  0,  0, 0, 0, 0),
      'look_down':    _action(  0, -10,  0,  0, 0, 0, 0),
      'strafe_left':  _action(  0,   0, -1,  0, 0, 0, 0),
      'strafe_right': _action(  0,   0,  1,  0, 0, 0, 0),
      'forward':      _action(  0,   0,  0,  1, 0, 0, 0),
      'backward':     _action(  0,   0,  0, -1, 0, 0, 0),
      'fire':         _action(  0,   0,  0,  0, 1, 0, 0),
      'jump':         _action(  0,   0,  0,  0, 0, 1, 0),
      'crouch':       _action(  0,   0,  0,  0, 0, 0, 1)
  }

  ACTION_LIST = ACTIONS.values()

  @staticmethod
  def get_action_size():
    return 8
  
  def __init__(self):
    environment.Environment.__init__(self)

    level = 'seekavoid_arena_01'

    self._env = deepmind_lab.Lab(
      level,
      ['RGB_INTERLACED'],
      config={
        'fps': str(60),
        'width': str(84),
        'height': str(84)
      })
    self.reset()

  def reset(self):
    self._env.reset()
    obs = self._env.observations()['RGB_INTERLACED']
    self.last_observation = self._preprocess_frame(obs)
    
  def _preprocess_frame(self, image):
    image = image.astype(np.float32)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    image = image.reshape((84,84))
    image = image / 255.0
    return image

  def step(self, action):
    real_action = LabEnvironment.ACTION_LIST[action]
    
    reward = self._env.step(real_action, num_steps=4)
    terminal = not self._env.is_running()

    obs = self._env.observations()['RGB_INTERLACED']
    self.last_observation = self._preprocess_frame(obs)
    return self.last_observation, reward, terminal
