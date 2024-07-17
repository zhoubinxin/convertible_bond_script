from utils.config_utils import get_config


def main():
    config = get_config('dev')
    print(config.ctype)


if __name__ == '__main__':
    main()
