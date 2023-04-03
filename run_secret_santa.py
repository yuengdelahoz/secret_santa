import sys, os
import argparse
import numpy as np
import copy
from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType, Disposition
from sendgrid import SendGridAPIClient
from time import sleep

from ss_email import EmailService
import json


def choose_secret_santa_for(name, pool):
	if len(pool) == 1:
		if name == pool[0]:
			raise Exception('incompatible pair')
	while True:
		np.random.shuffle(pool)
		selection = pool[0]
		if selection != name:
			return pool.pop(0)

def run_selection(players):
	is_complete = False
	max_len = 0
	for name in players:
		_len = len(name)
		if _len > max_len:
			max_len = _len
	pairs = {}
	while not is_complete:
		try:
			selection_pool = copy.deepcopy(players)
			for name in players:
				pairs[name] =  choose_secret_santa_for(name, selection_pool)
			is_complete = True
		except:
			pairs = {}

	return pairs

		

def load_players_info():
	players = dict()
	with open('players.csv','r') as fp:
		lines = fp.readlines()
		for line in lines:
			sline = line.strip()
			player, email, wishlist = sline.split(',')
			players[player.strip()]  = [email.strip(), wishlist.strip()]
	return players

def demo(pairs):
	email_service = EmailService()
	for name, secret_santa in pairs.items():
		player = {}
		player['name'] = name
		player['email'] = 'ysdelahoz@gmail.com'
		player['secret_santa'] = secret_santa
		player['ss_wishlist'] = players_info[secret_santa][1]
		email_service.send(player)

def real(pairs):
	email_service = EmailService()
	for name, secret_santa in pairs.items():
		print("revolviendo los papelitos...")
		sleep(3)
		# input(f"El secret santa de {name} ha sido seleccionado, presiona enter para enviar el correo a {name}.")
		player = {}
		player['name'] = name
		player['email'] = players_info[name][0]
		player['secret_santa'] = secret_santa
		player['ss_wishlist'] = players_info[secret_santa][1]
		email_service.send(player)
		# input("presiona enter para continuar")
		# os.system('clear')

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('--mode', type=str, required=True)
	args = parser.parse_args()
	os.system('clear')
	players_info = load_players_info()
	pairs = run_selection(list(players_info.keys()))

	if args.mode == "demo":
		demo(pairs)
	elif args.mode == "real":
		real(pairs)
