from project import Project
import src.config.setting as cfg
import logging

if __name__ == '__main__':
    logger = logging.getLogger()
    p = Project(cfg.SetUp)
    p.run()

