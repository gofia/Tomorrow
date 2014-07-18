import copy
import numpy as np

from datetime import date, timedelta

from ._constants import OIL_PRICE_SINCE_2000
from .utils import add_months, make_plot, diff_months_abs, start_plot
from .models import CountryProduction
from .fit_logistic import (fit_d_logistic_r_k_p, get_d_logistic, get_logistic,
                           fit_cyclic_logistic)


class HubbertBacktest():
    def __init__(self):
        pass

    @classmethod
    def run(cls, name):
        ds, nks, ukks, ukfs, fs = [], [], [], [], []
        ukfs2008, nfs2008 = [], []
        d = date(year=2000, month=1, day=1)
        d_2008 = date(year=2008, month=1, day=1)
        d_max = date.today() - timedelta(days=120)
        r = -1.0
        k = 20E9
        p = 1E8
        r1 = 0.03
        k1 = 10E9
        p1 = 4E9
        t1 = 120
        r2 = 0.03
        k2 = 10E9
        p2 = 5E9
        t2 = 300

        while d < d_max:
            # Norway
            ncps = CountryProduction.objects.filter(
                name="NO",
                date__lte=d,
            ).order_by("date")
            cops = np.array(map(lambda x: x.production_oil, ncps))
            months = np.array(range(0, len(cops)))
            r, k, p, residual = fit_d_logistic_r_k_p(months, cops, r, k, p)
            ds.append(copy.copy(d))
            nks.append(k)
            fs.append(k - get_logistic(r, k, p)(
                len(cops) + diff_months_abs(d_max, d)
            ))
            if d <= d_2008:
                nfs2008.append(get_logistic(r, k, p)(
                    len(cops) + diff_months_abs(d_max, d)
                ) - get_logistic(r, k, p)(
                    len(cops) + diff_months_abs(d_2008, d)
                ))
            print "{0}: {1}".format(d, k)

            # UK
            cps = CountryProduction.objects.filter(
                name="UK",
                date__lte=d,
            ).order_by("date")
            cops = np.array(map(lambda x: x.production_oil, cps))
            months = np.array(range(0, len(cops)))
            r1, k1, p1, t1, r2, k2, p2, t2, residual = fit_cyclic_logistic(
                months, cops, r1, k1, p1, t1, r2, k2, p2, t2
            )
            ukks.append(k1 + k2)
            ukfs.append(k1 - get_logistic(r1, k1, p1)(
                len(cops) + diff_months_abs(d_max, d) - t1
            ) + k2 - get_logistic(r2, k2, p2)(
                len(cops) + diff_months_abs(d_max, d) - t2
            ))
            if d <= d_2008:
                ukfs2008.append(get_logistic(r1, k1, p1)(
                    len(cops) + diff_months_abs(d_max, d) - t1
                ) + get_logistic(r2, k2, p2)(
                    len(cops) + diff_months_abs(d_max, d) - t2
                ) - get_logistic(r1, k1, p1)(
                    len(cops) + diff_months_abs(d_2008, d) - t1
                ) - get_logistic(r2, k2, p2)(
                    len(cops) + diff_months_abs(d_2008, d) - t2
                ))
            print "{0}: {1}".format(d, k1 + k2)

            d = add_months(d, 1)

        # make_plot(
        #     months,
        #     cops,
        #     "Months",
        #     "Production",
        #     months,
        #     get_d_logistic(r1, k1, p1)(months - t1) + get_d_logistic(r2, k2, p2)(months - t2)
        # )
        # make_plot(ds, ks, "Month", "K")


        # plt, ax1, ax2 = start_plot(
        #     "Back-testing date",
        #     "Remaining production (barrels)",
        #     "Remaining recoverable reserves in 2014\nA back-test using Hubbert"
        # )
        # print "{0} vs {1}".format(fs[0:2], fs[-2:-1])
        # print "{0} vs {1}".format(ukfs[0:2], ukfs[-2:-1])
        # print "{0} vs {1}".format(ukks[0], ukks[-1])
        # print "{0} vs {1}".format(nks[0], nks[-1])
        # l1 = ax1.plot(ds, fs, '-b', label="Forecast Norway")
        # l2 = ax1.plot(ds, ukfs, '-g', label="Forecast UK")
        # l3 = ax2.plot(ds, OIL_PRICE_SINCE_2000[:len(ds)], '-r', label="Oil price ($)")
        # ax1.set_ylim((0, 4E9))
        # ax2.set_ylabel("Oil price ($)")
        # ax1.legend(l1 + l2 + l3, ("Forecast Norway", "Forecast UK", "Oil price"), loc='upper left')
        # plt.show()

        print "{0}".format(fs[len(nfs2008)])
        print "{0}".format(ukfs[len(nfs2008)])

        plt, ax1, ax2 = start_plot(
            "Back-testing date",
            "Remaining production (barrels)",
            "Remaining recoverable reserves in 2014\nA back-test using Hubbert"
        )
        print "{0} vs {1}".format(nfs2008[0:2], nfs2008[-2:-1])
        print "{0} vs {1}".format(ukfs2008[0:2], ukfs2008[-2:-1])
        l1 = ax1.plot(ds[:len(nfs2008)], nfs2008, '-b', label="Forecast Norway")
        l2 = ax1.plot(ds[:len(ukfs2008)], ukfs2008, '-g', label="Forecast UK")
        l3 = ax2.plot(ds[:len(ukfs2008)], OIL_PRICE_SINCE_2000[:len(ukfs2008)], '-r', label="Oil price ($)")
        ax2.set_ylabel("Oil price ($)")
        ax1.legend(l1 + l2 + l3, ("Forecast Norway", "Forecast UK", "Oil price"), loc='upper left')
        plt.show()
