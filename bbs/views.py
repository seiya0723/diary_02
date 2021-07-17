from django.shortcuts import render,redirect
from django.views import View


from .models import Topic
from .forms import TopicForm,YearMonthForm

import datetime 


class BbsView(View):

    def get(self, request, *args, **kwargs):
        form    = YearMonthForm(request.GET)

        #フォームクラスを使用してバリデーションをすることで、数値以外のyearとmonthが指定された場合、未指定の場合はバリデーションNGとなり、elseに行く。
        if form.is_valid():
            validated   = form.validated_data

            print(validated["month"])
            print(validated["year"])

            topics  = Topic.objects.filter(dt__year=validated["year"],dt__month=validated["month"])
            dt      = datetime.date(int(validated["year"]),int(validated["month"]),1)
        else:

            #TODO:年と月の指定がない場合、今月の指定をするべきでは？
            topics  = Topic.objects.all()

            dt      = datetime.datetime.now()
            dt      = dt.replace(day=1)

        #topicsの中にある日付のリストを作る
        topic_dts   = []
        for topic in topics:
            topic_dts.append(str(topic.dt.year) + str(topic.dt.month) + str(topic.dt.day))

        year        = dt.year
        month       = dt.month
        days        = []
        weekdays    = []

        #.weekday()で数値化した曜日が出力される(月曜日が0、日曜日が6)
        #一ヶ月の最初が日曜日であればそのまま追加、それ以外の曜日であれば、曜日の数値に1追加した数だけ空文字を追加
        if dt.weekday() != 6:
            for i in range(dt.weekday()+1):
                weekdays.append("")

        #1日ずつ追加して月が変わったらループ終了
        while month == dt.month:
            dic = { "num":"","id":"" }

            #カレンダーの日付に投稿した日記がある場合、idに年月日の文字列型をセットする。(このidがリンクになる)
            for topic_dt in topic_dts:
                str_dt  = str(year) + str(month) + str(dt.day)
                if topic_dt == str_dt:
                    dic["id"]   = str_dt
                    break

            dic["num"]  = dt.day

            weekdays.append(dic)

            dt  = dt + datetime.timedelta(days=1)
            if dt.weekday() == 6:
                days.append(weekdays)
                weekdays    = []

        if dt.weekday() != 6:
            days.append(weekdays)
            weekdays    = []

        print(days)

        """
        [ ['  ', '  ', '1 ', '2 ', '3 ', '4 ', '5 '],
          ['6 ', '7 ', '8 ', '9 ', '10', '11', '12'],
          ['13', '14', '15', '16', '17', '18', '19'],
          ['20', '21', '22', '23', '24', '25', '26'],
          ['27', '28', '29', '30']
          ]
        """

        context = { "topics":topics,
                    "days":days,
                    "year":year,
                    "month":month,
                }

        return render(request,"bbs/index.html",context)

    def post(self, request, *args, **kwargs):

        form    = TopicForm(request.POST)

        if form.is_valid():
            print("バリデーションOK")
            form.save()
        else:
            print("バリデーションNG")

        return redirect("bbs:index")



index   = BbsView.as_view()

