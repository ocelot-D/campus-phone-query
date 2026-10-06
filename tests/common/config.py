"""
配置加载器：读取 env.yaml，提供当前环境的 base_url
"""
import os
import yaml

CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config', 'env.yaml')


class Config:
    def __init__(self, env_name=None):
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)

        self.env = env_name or data.get('active_env', 'dev')
        env_config = data[self.env]
        self.base_url = env_config['base_url'].rstrip('/')
        self.timeout = env_config.get('timeout', 10)

    def __repr__(self):
        return f"<Config env={self.env} base_url={self.base_url}>"


# 全局配置实例
config = Config()
