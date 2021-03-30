#!/usr/bin/env python3

import os

import click
import requests


@click.command()
@click.argument('state')
@click.option('--city', '-c', required=False, help='City Name.', type=str)
def main(state, city):
    # normalize some stuff
    state = state.upper()
    city = city.upper() if city else city
    cities = {}

    # make request and get JSON
    # status: "Available" / "Fully booked"
    r = requests.get(
        f'https://www.cvs.com/immunizations/covid-19-vaccine.vaccine-status.{state}.json?vaccineinfo',
        headers={
            'Host': 'www.cvs.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0',
            'Accept': 'application/json',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Referer': 'https://www.cvs.com/immunizations/covid-19-vaccine',
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'TE': 'Trailers'
        })

    if r.status_code == 200:
        time_stamp = r.json()['responsePayloadData']['currentTime']
        cities = r.json()['responsePayloadData']['data'][state]
        cities.sort(key=lambda x: x['city'])
        cities = {x['city']: x for x in cities}
    else:
        raise click.ClickException(f'Bad status getting state data. Status: {r.status_code} - {r.text}')

    # print whate we need
    if (city) and (city in cities) :
        click.echo(f"{city.title()}, {cities[city]['state']} - Status: {cities[city]['status']}")
        notify(state, [cities[city], ])
    else:
        for k, v in cities.items():
            click.echo(f"{k.title()}, {v['state']} - Status: {v['status']}")

        notify(state, list(cities.values()))


def notify(state, cities):
    available = [f'{x["city"].title()}, {state}' for x in cities if x['status'].lower() == 'available']

    click.echo()
    click.echo()
    if not(available):
        click.echo(f'No appointments available in {state}.')
    else:
        click.echo(f'Vaccine appointments available in {state} at: ')
        click.echo ("\n".join(available))


if __name__ == '__main__':
    main()
