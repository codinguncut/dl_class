import pystk

pystk.set_log_level(0)
config = pystk.GraphicsConfig.none()
config.screen_width = 800
config.screen_height = 600
pystk.init(config)
