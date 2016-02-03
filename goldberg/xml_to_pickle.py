#! /usr/bin/python
# -*- coding: utf-8 -*-
import cPickle as pickle
from bs4 import BeautifulSoup


def height(pitch):
    """ Calculate absolute height of given pitch. """
    # pitch example: [u'G', u'5']
    cde_list = ["c","d","e","f","g","a","b"]
    h =  int(pitch[1])*7
    h += cde_list.index(pitch[0].lower())
    return h

def extract_music(soup):
    """ Extract music data from xml file. """
    pitch_list = []
    end_times = []
    cur_time = 0 # Current time
    tmp_duration = 0
    # parse
    for m in soup.find_all("measure"):
        for nb in m.find_all({"note", "backup", "direction"}):
            if nb.name == "backup": # 巻き戻し
                cur_time -= int(nb.duration.string)
            if nb.name == "note":
                if not nb.chord: # 和音でなければ
                    cur_time += tmp_duration
                if nb.pitch: # 音符
                    pitch_list.append([cur_time,
                                       nb.pitch.step.string, 
                                       nb.pitch.octave.string])
                if nb.rest: # 休符
                    pass
                if nb.duration: # 装飾音はdurationないので飛ばす
                    tmp_duration = int(nb.duration.string)
            if nb.name=="direction": # 
                if (not end_times) or cur_time > end_times[-1]:
                    end_times.append(cur_time)
    end_times[0] = -1 # 便宜的に
    return pitch_list, end_times


if __name__ == "__main__":
    xml_name = "goldberg_full.xml"# CC Zero xml: Open Goldberg
    soup = BeautifulSoup(open(xml_name,'r').read(), "lxml")
    
    pitch_list, end_times = extract_music(soup)
    
    # split pitch_list
    pitch_list = sorted(pitch_list, key=lambda x: x[0])
    times = [p[0] for p in pitch_list]
    pitches = [height(p[1:]) for p in pitch_list]

    # save pickle
    pickle_file = 'goldberg_full.pickle'
    try:
        f = open(pickle_file, 'wb')
        save = {
            'times': times,
            'pitches': pitches,
            'end_times': end_times,
        }
        pickle.dump(save, f, pickle.HIGHEST_PROTOCOL)
        f.close()
    except Exception as e:
        print 'Unable to save data to', pickle_file, ':', e
        raise
