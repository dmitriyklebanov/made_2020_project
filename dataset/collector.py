from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest

import argparse
import configparser
import pandas as pd


async def dump_all_messages(client, channel, output_file, limit=None):
    offset_msg = 0
    all_messages = []

    while True:
        history = await client(GetHistoryRequest(
            peer=channel,
            offset_id=offset_msg,
            offset_date=None,
            add_offset=0,
            limit=100,  # for one request
            min_id=0,
            max_id=0,
            hash=0,
        ))
        if not history.messages:
            break
        messages = history.messages
        for message in messages:
            all_messages.append(message.to_dict())
        offset_msg = messages[len(messages) - 1].id
        if limit and len(all_messages) >= limit:
            break

    df = pd.DataFrame(all_messages)
    df.to_csv(output_file)
    return df


async def process_url(client, url, output_file):
    channel = await client.get_entity(url)
    await dump_all_messages(client, channel, output_file)


def get_user_config(config_filename):
    config = configparser.ConfigParser()
    config.read(config_filename)
    config = config['Telegram']
    return {key: config[key] for key in ('session', 'api_id', 'api_hash')}


def main(args):
    config = get_user_config(args.config_file)
    client = TelegramClient(**config)
    client.start()
    with client:
        client.loop.run_until_complete(process_url(
            client,
            args.channel_url,
            args.output_file
        ))


def make_parser(parser):
    parser.description = 'Collect all messages from certain telegram channel'
    parser.add_argument('--config-file', type=str, required=False,
                        default='dataset/config.ini', help='path to config file')
    parser.add_argument('--output-file', type=str, required=False,
                        default='dataset/raw_messages.csv', help='path to output file')
    parser.add_argument('--channel-url', type=str, required=True,
                        help='path to output file')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    make_parser(parser)
    main(parser.parse_args())
