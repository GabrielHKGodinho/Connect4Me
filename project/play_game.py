import connect_four as cf
import connect_four_Algorithm as CFA

CFA.dificuldade = 0
while CFA.dificuldade < 1 or CFA.dificuldade > 3:
    CFA.dificuldade = input("1- Facil 2- Médio 3- Dificil: ")
    CFA.dificuldade = int(CFA.dificuldade)
if CFA.dificuldade == 1:
    CFA.dificuldade = 3
elif CFA.dificuldade == 2:
    CFA.dificuldade = 5
else:
    CFA.dificuldade = 19

cf.starter = 0
while cf.starter < 1 or cf.starter > 2:
    cf.starter = input("Quem comeca? 1- Voce 2- Coelho: ")
    cf.starter = int(cf.starter)

cf_object = cf.Connect_Four(log = True)
cf_Algorithm = CFA.Connect_four_algorithm()

cf_object.play_game(cf_object.real_player_opencv, cf_Algorithm.min_max_alpha_beta_player, log = True)