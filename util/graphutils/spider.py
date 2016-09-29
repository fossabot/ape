import numpy as np
import pylab as pl
import sys
from pymongo import MongoClient

class Radar(object):

    def __init__(self, fig, titles, labels, rect=None):
        if rect is None:
            rect = [0.05, 0.05, 0.95, 0.95]

        self.n = len(titles)
        self.angles = np.arange(90, 90+360, 360.0/self.n)
        self.axes = [fig.add_axes(rect, projection="polar", label="axes%d" % i)
                         for i in range(self.n)]

        self.ax = self.axes[0]
        self.ax.set_thetagrids(self.angles, labels=titles, fontsize=14)

        for ax in self.axes[1:]:
            ax.patch.set_visible(False)
            ax.grid("off")
            ax.xaxis.set_visible(False)

        for ax, angle, label in zip(self.axes, self.angles, labels):
            ax.set_rgrids(range(1, 6), angle=angle, labels=label)
            ax.spines["polar"].set_visible(False)
            ax.set_ylim(0, 5)

    def plot(self, values, *args, **kw):
        angle = np.deg2rad(np.r_[self.angles, self.angles[0]])
        values = np.r_[values, values[0]]
        self.ax.plot(angle, values, *args, **kw)

def generateGraphs():
    titles = ["loc", "SWD", "SVD", "SMD", "CVSS", "files"]
    labels = [
                list("abcdef"), list("123456"), list("uvwxyz"),
                ["one", "two", "threes", "four", "five", "six"],
                list("jklmno")
            ]
    fig = pl.figure(figsize=(6, 6))
    radar = Radar(fig, titles, labels)


    upload_id = ''
    project_tag = ''


    cmap = ["red", "green"]
    for each_ape_row in apepackage.find():
        upload_id = each_ape_row['upload_id']
        upload_info = uploads.find_one({'_id': upload_id})
        project_tag = upload_info['project_tag']
        radar.plot([each_ape_row['intrinsic_total_code'],
                each_ape_row['intrinsic_cwe_density'],
                each_ape_row['extrinsic_cwe_density'],
                each_ape_row['instrinsic_sig_density'],
                each_ape_row['extrinsic_cvss_max'],
                each_ape_row['intrinsic_files']
               ],
               "-", lw=2, color="1,1,1", alpha=0.6, label='')
        #cmap.remove[cmap[0]]
    radar.ax.legend()
    pl.savefig('fig.png')

if __name__ == '__main__':
    client = MongoClient()
    db = client.apedb
    uploads = db.uploads
    apepackage = db.apepackage

    generateGraphs()
