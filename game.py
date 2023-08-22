import pyxel
import math
import random

class GameStart:
    def __init__(self):
        self.difficulty = 0
        self.question = 0
        self.questions = ['Did you brush your teeth after a meal?', 'Do you often go to the dentist?', 'KOIME NO AJITSUKE WA SUKI ?']
        self.choices = [[" Yes"," No"],[" Yes"," No"],["KIRAI","SUKI"]]
        self.center = [57,70,74]
    def start_update(self):
        if self.question < 3:
            if pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON) and (68 < pyxel.mouse_x < 108) and (110 < pyxel.mouse_y < 130):
                self.question += 1
            if pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON) and (148 < pyxel.mouse_x < 188) and (110 < pyxel.mouse_y < 130):
                self.difficulty += 1
                self.question += 1
        elif self.question == 3:
            pyxel.mouse(False)
            if pyxel.btnp(pyxel.KEY_SPACE):
                self.question +=1
                App.game = True
        else:
            pass
    def start_draw(self):
        if self.question < 3:
            pyxel.rect(68, 110, 40, 20, 11)
            pyxel.rect(148, 110, 40, 20, 11)
            pyxel.text(95, 30, "HEALTH CHECK  "+ str(self.question+1)+"/3", 0)
            pyxel.text(self.center[self.question], 70, self.questions[self.question], 0)
            pyxel.text(79, 117, self.choices[self.question][0], 0)
            pyxel.text(161, 117, self.choices[self.question][1], 0)
            pyxel.mouse(True)
        elif self.question == 3:
            pyxel.blt(120, 90, 0, 16, 0, 16, 15, 12)
            pyxel.text(105, 65, "^", 0)
            pyxel.text(105, 65, "| KEY : jump", 0)
            pyxel.text(25, 97, "<- KEY : move left", 0)
            pyxel.text(160, 97, "-> KEY : move right", 0)
            pyxel.text(64,150,"PRESS SPACE KEY TO START THE GAME", 0)
        else:
            pass


class App:
    start = GameStart()
    game = False
    def __init__(self):
        pyxel.init(256, 200)#, title="IREBA GAME"
        pyxel.load("ireba_game.pyxres")#assets/
        #BGM
        pyxel.sound(0).set("e2e2c2g1 g1g1c2e2 d2d2d2g2 g2g2rr" "c2c2a1e1 e1e1a1c2 b1b1b1e2 e2e2rr","p","6","vffn fnff vffs vfnn",25,)
        pyxel.sound(1).set("r a1b1c2 b1b1c2d2 g2g2g2g2 c2c2d2e2" "f2f2f2e2 f2e2d2c2 d2d2d2d2 g2g2r r ","s","6","nnff vfff vvvv vfff svff vfff vvvv svnn",25,)
        pyxel.sound(2).set("c1g1c1g1 c1g1c1g1 b0g1b0g1 b0g1b0g1" "a0e1a0e1 a0e1a0e1 g0d1g0d1 g0d1g0d1","t","7","n",25,)
        pyxel.sound(3).set("f0c1f0c1 g0d1g0d1 c1g1c1g1 a0e1a0e1" "f0c1f0c1 f0c1f0c1 g0d1g0d1 g0d1g0d1","t","7","n",25,)
        pyxel.sound(4).set("f0ra4r f0ra4r f0ra4r f0f0a4r", "n", "6622 6622 6622 6422", "f", 25)

        self.score = 0
        self.miss = 0
        self.clear = 0

        #メインキャラクター関連
        self.player_x = 0
        self.player_y = 100
        self.player_y_v = 0
        self.player_y_a = 1
        self.jump = 11
        self.direction = 16

        #敵キャラ,コイン,ステージ関連
        self.enemy_x = [[239],[80,112],[80,112],[], [], [], [240], []]
        self.enemy_y = [[152],[152,152],[104,56],[], [], [], [168], []]
        self.enemy_direction = [[random.choice([-1,1])],[1,1],[1,1],[], [], [], [1], []]
        self.enemy_y_v = [[0],[0,0],[0,0],[], [], [], [0], []]
        self.enemy_y_a = 1
        self.killer_x = 280
        self.teresa = [[80,120,0,16],[224,56,0,16]]
        self.toge = [[],[],[],[],[[200,160],[200,128],[200,112]],[[40,104],[80,144],[112,152],[144,120],[184,120],[184,136],[200,120],[216,120]],[],[]]
        self.block = [[[64,120,32],[128,120,32],[144,72,32],[160,120,32]], [], [[80,120,32]], [[112,136,32]],[[144,136,32]], [[128,136,32]], [[32,96,32],[112,136,32],[136,80,32],[160,136,32]], [], []]
        self.coin = [[[160,150],[184,150],[208,150]],[[192,128]],[[224,80]],[[128,72]],[[80,112],[208,100]],[[224,168]],[[136,136],[192,80]],[[200,25]]]
        self.appear = 0
        self.appear_coin = []

        #タイルマップ関連,横スクロールではなく場面転換式
        self.stage = 0  #クリア画面見るなら７にする
        self.skip = 0
        self.background = 12

        self.play_music()
        pyxel.run(self.update, self.draw)
    def play_music(self):
        pyxel.play(0, [0, 1], loop=True)
        pyxel.play(1, [2, 3], loop=True)
        pyxel.play(2, 4, loop=True)

    def update(self):
        if App.game == True:
            if self.clear == 0:
                self.move_player()
                self.move_enemy()
            else:
                pass
        else:
            App.start.start_update()

    def draw(self):
        pyxel.cls(self.background)
        if App.game == True:
            if self.clear < 100:
                self.tilemap_draw()
                pyxel.text(0,0,'score: ' + str(self.score),0)
                pyxel.text(40,0,'miss: ' + str(self.miss),0)
                #str(self.get_distance(self.enemy_x[0]+7,self.enemy_y[0]+7))
                self.draw_coin()
                self.draw_block()
                self.draw_toge()
                if self.stage == 2:
                    self.draw_killer()
                if self.stage ==4:
                    self.draw_teresa()
                for i in range(0,len(self.enemy_x[self.stage])):
                    pyxel.blt(self.enemy_x[self.stage][i], self.enemy_y[self.stage][i], 0, 32, 32, 16, 16, 12)
                pyxel.blt(self.player_x, self.player_y, 0, self.direction, 0, 16, 15, 12)
                if self.stage == 7:
                    self.game_clear(App.start)
                if self.skip >= 10:
                    self.skip_stage()
            else:
                self.game_clear(App.start)
        else:
            App.start.start_draw()
#(コピー先x, コピー先y, イメージバンク番号, イメージバンクx, イメージバンクy, イメージバンク領域x, イメージバンク領域y, 透過する色コード)

    def tilemap_draw(self):
        base_x = 0
        base_y = 72
        u = 0 + self.stage*32
        v = 0
        # 指定したtm(template)番号の(u,v)座標からサイズ(w,h)の大きさを(base_x,base_y)座標に描画する
        pyxel.bltm(base_x,base_y,0,u,v,32,16)


#Player
    def move_player(self):
        #左方向への移動
        if pyxel.btn(pyxel.KEY_LEFT):
            if pyxel.pget(self.player_x - 1, self.player_y) == self.background and pyxel.pget(self.player_x - 1, self.player_y + 14) == self.background and pyxel.pget(self.player_x - 1, self.player_y + 6) == self.background:
                self.player_x -= 2
                self.direction = 32
        #右方向への移動
        if pyxel.btn(pyxel.KEY_RIGHT):
            if pyxel.pget(self.player_x + 16, self.player_y) == self.background and pyxel.pget(self.player_x + 16, self.player_y + 14) == self.background and pyxel.pget(self.player_x + 16, self.player_y + 6) == self.background:
                self.player_x += 2
                self.direction = 16

#どっちかが背景じゃなかったら（＝床だったら）実行されない
#どっちも背景の時（空中）
        if pyxel.pget(self.player_x, self.player_y + 15) == self.background and pyxel.pget(self.player_x + 15, self.player_y + 15) == self.background:
            #空中かつ上昇中,ジャンプの高さ調節
            if self.player_y_v < 0:
                if pyxel.btn(pyxel.KEY_UP) and self.jump != 0 and self.jump <= 7:
                    self.jump += 1
                    self.player_y_v = -6
                if pyxel.btnr(pyxel.KEY_UP):
                    self.jump = 11
                #天井判定
                for i in range (1,7):
                    if pyxel.pget(self.player_x, self.player_y - i) == self.background and pyxel.pget(self.player_x + 15, self.player_y - i) == self.background:
                        pass
                    else:
                        self.player_y += 1 - i
                        self.jump = 11
                        self.player_y_v = 0
                        pyxel.play(3,7,loop=False)
                        self.hatenablock()
                        break
            #着地(地面に近い空中かつ下降中),判定（ジャンプ可能判定を与える）
            for i in range (1, 6):
                if pyxel.pget(self.player_x, self.player_y + 15 + i) == self.background and pyxel.pget(self.player_x + 8, self.player_y + 15 + i) == self.background and pyxel.pget(self.player_x + 15, self.player_y + 15 + i) == self.background:
                    pass
                else:
                    if self.player_y_v >0:
                        self.player_y += i
                        self.jump = 0
                        self.player_y_v = 0
                        break
        #上昇下降問わず空中（地面からはある程度離れている）
        if pyxel.pget(self.player_x, self.player_y + 15) == self.background and pyxel.pget(self.player_x + 8, self.player_y + 15) == self.background and pyxel.pget(self.player_x + 15, self.player_y + 15) == self.background:
            self.player_y_v += self.player_y_a
            if self.player_y_v >= 5:
                self.player_y_v = 5
            self.player_y += self.player_y_v
#床にいる時
        #ジャンプ
        elif pyxel.btnp(pyxel.KEY_UP):
            self.jump = 1
            self.player_y_v = -5
            self.player_y += self.player_y_v
            pyxel.play(3,6)
        #穴に落ちた時
        if self.player_y >= 185 :
            self.miss +=1
            pyxel.play(3,9,loop=False)
            self.restart()
    #ステージ移動
        if self.player_x >= 240:
            self.stage += 1
            self.restart()
            self.skip = 0
#ここまでプレイヤーの動き関連

    def restart(self):
        self.player_x = 0
        self.player_y = 100
        self.player_y_v = 0
        self.player_y_a = 1
        self.jump = 11
        self.direction = 16
        self.skip += 1
        if self.stage ==4:
            self.teresa = [[80,120,0,16],[224,56,0,16]]
    def skip_stage(self):
        pyxel.text(100, 0, "PRESS SPACE KEY TO SKIP THE STAGE", 0)
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.stage += 1
            self.restart()
            self.skip = 0

#距離を計算する
    def get_distance(self, x2, y2):
        d = math.sqrt((x2 - (self.player_x+7)) ** 2 + (y2 - (self.player_y+7)) ** 2)
        return d
#ハテナブロック叩いた時
#pyxel.tilemap(0).set(App.enemy_x[0],App.enemy_y[0],["000000"])
    def hatenablock(self):
        for i in range(0,len(self.block[self.stage])):
            if (self.block[self.stage][i][0] <= self.player_x+7 <= self.block[self.stage][i][0]+15) and (self.block[self.stage][i][1]+17> self.player_y > self.block[self.stage][i][1]) and (self.block[self.stage][i][2] == 32):
                self.block[self.stage][i][2] = 48
                self.score +=1
                pyxel.play(3,5,loop=False)
                self.appear = 30
                self.appear_coin.append(int(self.block[self.stage][i][0]))
                self.appear_coin.append(int(self.block[self.stage][i][1] - 8))
    def draw_block(self):
        for i in range(0,len(self.block[self.stage])):
            pyxel.blt(self.block[self.stage][i][0], self.block[self.stage][i][1], 0, self.block[self.stage][i][2], 16, 16, 16, 12)
    def draw_coin(self):
        for i in range(0,len(self.coin[self.stage])):
            #コインゲット
            if self.get_distance(self.coin[self.stage][i][0]+7,self.coin[self.stage][i][1]+8) <= 15.4 and self.coin[self.stage][i][0] >= 0:
                self.coin[self.stage][i][0] = -20
                self.score += 1
                pyxel.play(3,5,loop=False)
            pyxel.blt(self.coin[self.stage][i][0], self.coin[self.stage][i][1], 0, 16, 32, 16, 16,12)
            if self.appear >0:
                self.appear -= 1
                self.appear_coin[1] -= 0.3
                pyxel.blt(self.appear_coin[0], self.appear_coin[1], 0, 16, 32, 16, 16,12)
            else:
                self.appear_coin = []
    def draw_toge(self):
        for i in range(0,len(self.toge[self.stage])):
            #トゲに当たったかどうかの判定
            if self.get_distance(self.toge[self.stage][i][0]+7,self.toge[self.stage][i][1]+7) <= 15.7:
                self.miss += 1
                pyxel.play(3,9,loop=False)
                self.restart()
            pyxel.blt(self.toge[self.stage][i][0], self.toge[self.stage][i][1], 0, 32, 64, 16, 16,12)
    def draw_teresa(self):
        for i in range(0,2):
            #動くか動かないか、
            if self.player_x < self.teresa[i][0]:
                self.teresa[i][3] = 16
                #プレイヤーが背を向ければ動く
                if self.direction == 32:
                    self.teresa[i][2]=16
                    self.teresa[i][0]-=0.3
                    if self.player_y >self.teresa[i][1]:
                        self.teresa[i][1]+=0.3
                    else:
                        self.teresa[i][1]-=0.3
                else:
                    self.teresa[i][2]=0
            else :
                self.teresa[i][3] = -16
                if self.direction == 16:
                    self.teresa[i][2]=16
                    self.teresa[i][0]+=0.3
                    if self.player_y >self.teresa[i][1]:
                        self.teresa[i][1]+=0.3
                    else:
                        self.teresa[i][1]-=0.3
                else:
                    self.teresa[i][2]=0
            #テレサに当たったかどうかの判定
            if self.get_distance(self.teresa[i][0]+7,self.teresa[i][1]+7) <= 18:
                self.miss += 1
                self.teresa = [[80,120,0,16],[224,56,0,16]]
                pyxel.play(3,9,loop=False)
                self.restart()
            pyxel.blt(self.teresa[i][0], self.teresa[i][1], 0, self.teresa[i][2], 48, self.teresa[i][3], 16,12)

    def move_enemy(self):
        for i in range(0,len(self.enemy_x[self.stage])):
            if self.enemy_x[self.stage][i] < 0:
                pass
            else:
                #左右の方向転換
                if pyxel.pget(self.enemy_x[self.stage][i] - 1, self.enemy_y[self.stage][i] + 14) != self.background and self.enemy_direction[self.stage][i] == 1:
                    self.enemy_direction[self.stage][i] *= -1
                if pyxel.pget(self.enemy_x[self.stage][i] + 16, self.enemy_y[self.stage][i] + 14) != self.background and self.enemy_direction[self.stage][i] == -1:
                    self.enemy_direction[self.stage][i] *= -1
                self.enemy_x[self.stage][i] += -1 * self.enemy_direction[self.stage][i]
                #落下(プレイヤーの挙動と同じ)
                if pyxel.pget(self.enemy_x[self.stage][i], self.enemy_y[self.stage][i] + 16) == self.background and pyxel.pget(self.enemy_x[self.stage][i] + 15, self.enemy_y[self.stage][i] + 16) == self.background:
                    for j in range (1, 6):
                        if pyxel.pget(self.enemy_x[self.stage][i], self.enemy_y[self.stage][i] + 16 + j) == self.background and pyxel.pget(self.enemy_x[self.stage][i] + 8, self.enemy_y[self.stage][i] + 16 + j) == self.background and pyxel.pget(self.enemy_x[self.stage][i] + 16, self.enemy_y[self.stage][i] + 16 + j) == self.background:
                            pass
                        else:
                            if self.enemy_y_v[self.stage][i] >0:
                                self.enemy_y[self.stage][i] += j
                                self.enemy_y_v[self.stage][i] = 0
                                break
                if pyxel.pget(self.enemy_x[self.stage][i], self.enemy_y[self.stage][i] + 16) == self.background and pyxel.pget(self.enemy_x[self.stage][i] + 8, self.enemy_y[self.stage][i] + 16) == self.background and pyxel.pget(self.enemy_x[self.stage][i] + 15, self.enemy_y[self.stage][i] + 16) == self.background:
                    self.enemy_y_v[self.stage][i] += self.enemy_y_a
                    if self.enemy_y_v[self.stage][i] >= 5:
                        self.enemy_y_v[self.stage][i] = 5
                    self.enemy_y[self.stage][i] += self.enemy_y_v[self.stage][i]
                if self.enemy_y[self.stage][i] >= 184:
                    self.enemy_x[self.stage][i] = -20
            #敵を踏んだ時
            if abs(self.enemy_x[self.stage][i] - self.player_x) < 15 and self.enemy_y[self.stage][i] -16 <= self.player_y <= self.enemy_y[self.stage][i]:
                self.player_y_v = -5
                self.score += 1
                self.enemy_x[self.stage][i] = -20
                pyxel.play(3,8,loop=False)
            #敵に触れてしまった時
            if (abs(self.enemy_x[self.stage][i] - self.player_x) <= 16 and (self.enemy_y[self.stage][i] < self.player_y + 7 < self.enemy_y[self.stage][i] + 16)) or (abs(self.enemy_y[self.stage][i] - self.player_y) <= 16 and (self.enemy_x[self.stage][i] -15 < self.player_x < self.enemy_x[self.stage][i] + 15)):
                self.miss += 1
                pyxel.play(3,9,loop=False)
                self.restart()
    def draw_killer(self):
        if abs(self.killer_x - self.player_x) < 16 and (104-self.player_y <= 15)and self.player_y <102:
            self.player_y_v = -5
            self.player_y -=1
        elif (abs(self.killer_x - self.player_x) <= 16 and (104 < self.player_y + 7 < 118)) or (abs(104 - self.player_y) <= 16 and (self.killer_x -15 < self.player_x < self.killer_x + 15)):
            self.miss +=1
            if self.killer_x <30:
                self.killer_x = 256
            pyxel.play(3,9,loop=False)
            self.restart()
        if self.killer_x < -20 :
            self.killer_x = 256
        self.killer_x -= 1
        pyxel.blt(self.killer_x, 104, 0, 48, 32, 16, 16,12)

    def game_clear(self,start):
        if self.player_x >=224 and self.clear <99:
            self.clear += 1
            pyxel.rect(80,64,96,64,0)
            pyxel.text(106,84,"GAME CLEAR!",pyxel.frame_count % 16)
        elif self.clear == 99:
            pyxel.rect(80,64,96,64,0)
            pyxel.text(106,84,"GAME CLEAR!",pyxel.frame_count % 16)
            pyxel.text(64,104,"PRESS SPACE KEY TO CHECK THE RESULT", 7)
            if pyxel.btnp(pyxel.KEY_SPACE):
                self.clear += 1
        elif self.clear == 100:
            self.background = 0
            age = 70- 2*(self.score - self.miss) + start.difficulty - (153-self.player_y)//10
            pyxel.text(80,80,"Your teeth age is " + str(age), 7)
            pyxel.text(110,90,'score: ' + str(self.score),7)
            pyxel.text(110,95,'miss: ' + str(self.miss),7)
"""
cd assets
pyxeleditor ireba_game.pyxres
"""

App()
