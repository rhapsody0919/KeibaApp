import os 
import datetime
from flask import Flask, request, render_template
from scraiping import make_url, Scraiping
from helpers import Choise, Relative
from methods import Winning
import pandas as pd # => pip install pandas


# from flask import Flask, render_template
app = Flask(__name__)
port = int(os.environ['PORT'])

def run_Winning(c, sc_df):

    #combiの要素が一個の場合
    if type(c) == str:

        Wi = Winning(sc_df['単勝'], sc_df[c])
        model = Wi.model_0()

        return Wi.result(model)

    #combiの要素が二個の場合
    else:

        c0 = c[0]
        c1 = c[1]
        Wi = Winning(sc_df['単勝'], sc_df[c0], sc_df[c1])
        model = Wi.model_0()

        return Wi.result(model)

@app.route('/')
def index():
   return render_template('index.html')

@app.route('/result', methods=['POST'])
def post():
   input_date = request.form.get('date')
   tdate = datetime.datetime.strptime(input_date, '%Y-%m-%d')
   year = str(tdate.year)
   date = str(tdate.strftime('%m'))+str(tdate.strftime('%d'))
   place = str(request.form.get('place'))
   race = str(request.form.get('race')).zfill(2)
   #値をセット
   info = [year, place, date, race]
	#単勝用, 馬単用のurl作成
   tansyo_url, umatan_url = make_url(info)
	#スクレイピング開始
   if Scraiping(tansyo_url, umatan_url).get().empty:
      message = "レースが存在しませんでした"
      return render_template('result.html', message=message)
   else :
      sc_df = Scraiping(tansyo_url, umatan_url).get()
      #馬単合成オッズ計算
      re_df = Relative(sc_df).sum_odds()
      #class Winningに入れる馬単の引数の組み合わせを作成
      combi = Choise(re_df).combine()
      #combiが空の場合
      if combi == []:
         message = "Not Solved"
         return render_template('result.html', message=message)
      #combiがある場合
      else:
         #combiを使ってWinningを走らせる
         for c in combi:
            result = run_Winning(c, sc_df)
            print(str(c) + ':' + result[1])
            if result[1] == 'Solved':
               print(result[0])
               #最適解があれば結果を表示
               df_solved_values = result[0].values.tolist()
               df_solved_columns = result[0].columns.tolist()
               df_solved_columns.insert(0, '馬番')
               df_solved_index = result[0].index.tolist()
               return render_template('result.html', df_solved_values=df_solved_values, df_solved_columns=df_solved_columns, df_solved_index=df_solved_index)
            message = "Not Solved"
            return render_template('result.html', message=message)


if __name__ == '__main__':
   app.run(debug=True, host='0.0.0.0', port=port)
