class GoodsRecently(object):

    def __init__(self, request):

        self.request = request
        self.goods = []

        self.get()

    def set(self, good_id):

        if good_id in self.goods:
            self.goods.remove(good_id)

        if good_id not in self.goods and len(self.goods) >= 10:
            self.goods = self.goods[:-1]

        self.goods.insert(0, good_id)

        self.request.session['recent_goods'] = self.goods

    def get(self):

        if 'recent_goods' in self.request.session:
            self.goods = self.request.session['recent_goods']
