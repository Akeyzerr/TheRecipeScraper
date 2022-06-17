# coding: utf-8
from collections import OrderedDict

from modules.models.ingredient_entry import IngredientEntry
from modules.validators import validate_key_existing


class Ingredients(object):
    def __init__(self):
        self._ingredients = OrderedDict()

    def get_unique_count(self):
        rv = len(self._ingredients.keys())
        return rv

    def append(self, other):
        # type: (IngredientEntry) -> None
        if isinstance(other, IngredientEntry) and other.ingredient:
            validate_key_existing(self._ingredients, other.ingredient, [])
            self._ingredients[other.ingredient].append(other)

    def __contains__(self, item):
        return item in self._ingredients.keys()

    def __str__(self):
        return "Recipe Ingredients:\n\t{}".format(
            "\n\t".join(
                ["{}: {}".format(
                    k, ", ".join(
                        ["{} {}".format(q.quantity, q.unit) for q in vals])
                ) for k, vals in self._ingredients.items()]))

    def __len__(self):
        return sum([len(ingr) for ingr in self._ingredients.values()])

    def __lt__(self, other):
        if len(self) < len(other):
            return True
        elif len(self) == len(other):
            rv = False
            for k, v_lt in self._ingredients.items():
                if k in other:
                    rv = sum([v_sum.quantity for v_sum in self._ingredients[k]]) < \
                         sum([o.quantity for o in other[k]])
                    if rv:
                        return rv
            return rv

    def __gt__(self, other):
        if len(self) > len(other):
            return True
        elif len(self) == len(other):
            rv = False
            for k, v_gt in self._ingredients.items():
                if k in other:
                    rv = sum([v_gt_sum.quantity for v_gt_sum in self._ingredients[k]]) > \
                         sum([o.quantity for o in other[k]])
                    if rv:
                        return rv
            return rv

    def __le__(self, other):
        if len(self) <= len(other):
            return True
        elif len(self) == len(other):
            rv = False
            for k, v_le in self._ingredients.items():
                if k in other:
                    rv = sum([v_le_sum.quantity for v_le_sum in self._ingredients[k]]) <= \
                         sum([o.quantity for o in other[k]])
                    if rv:
                        return rv
            return rv

    def __eq__(self, other):
        return len(self) == len(other) \
               and self.get_unique_count() == other.get_unique_count()

    def __getitem__(self, item):
        return self._ingredients[item] if item in self._ingredients.keys() else None

    def __iter__(self):
        for k, v_iter in self._ingredients.items():
            yield k, v_iter


if __name__ == "__main__":
    tests1 = {
        "t1": IngredientEntry(u"кисело мляко - 100 мл"),
        "t2": IngredientEntry(u"закваска - 3/4 ч.ч."),
        "t3": IngredientEntry(u"кайма - 200 - 250 г"),
        "t4": IngredientEntry(u"нещо си - 250 гр."),
        "t5": IngredientEntry(u""),
        "t6": IngredientEntry(u"нещо си - 200 гр."),
    }
    tests2 = {
        "t1": IngredientEntry(u"кисело мляко - 50 мл"),
        "t2": IngredientEntry(u"закваска - 3/4 ч.ч."),
        "t3": IngredientEntry(u"кайма - 200 - 250 г"),
        "t4": IngredientEntry(u"нещо си - 250 гр."),
        "t5": IngredientEntry(u""),
        "t6": IngredientEntry(u"нещо си - 200 гр."),
    }
    # tests2 = {
    #     "t1": IngredientEntry(u"кисело зеле - 100 мл"),
    #     "t2": IngredientEntry(u"закваска - 1 ч.ч."),
    #     "t3": IngredientEntry(u"кайма - 400 гр"),
    #     "t4": IngredientEntry(u"нещо друго - 250 гр."),
    # }

    st1 = Ingredients()
    st2 = Ingredients()

    for _, v_tests in tests1.items():
        st1.append(v_tests)

    for _, v_tests in tests2.items():
        st2.append(v_tests)

    print(len(st1), len(st2))
    # print(st1["закваска"])
    # print(st1.get_unique_count())
    # for _, j in st1:
    #     print(j)

    # print(st1 > st2)
    print(st1)
    # print(st2)
    # mylist = [st2, st1, st1]
    # print(sorted(mylist, reverse=True))
