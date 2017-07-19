from subprocess import call
from os.path import exists, isfile, getsize

"""
CONFIG
"""

osmosis_cmd = './osmosis'

osm_types = [
    'nodes',
    'ways',
    'relations'
]

features = [
    ['amenity', 'hospital'],
    ['amenity', 'clinic']
]

continents = [
    'africa',
    'antarctica',
    'asia',
    'australia-oceania',
    'central-america',
    'europe',
    'north-america',
    'south-america'
]

base_url = 'http://download.geofabrik.de/'
extension = '.osm.pbf'

"""
SCRIPT
"""


def download(continent):
    if not exists(pbf_file) and not isfile(pbf_file):
      print 'Downloading %s' % continent
      url = '%s%s' % (base_url, pbf_file)
      call('wget %s' % url, shell=True)
    else:
      print 'Skipping download %s' % continent


def extract(key, value, osm, continent, output):
    print '%s = %s %s from %s' % (key, value, osm, continent)

    if osm == 'nodes':
        cmd = '%s ' \
              '--read-pbf %s ' \
              '--tf accept-nodes %s=%s ' \
              '--tf reject-ways ' \
              '--tf reject-relations ' \
              '--write-pbf %s' % (osmosis_cmd, pbf_file, key, value, output)
    elif osm == 'ways':
        cmd = '%s ' \
              '--read-pbf %s ' \
              '--tf accept-ways %s=%s ' \
              '--used-node ' \
              '--tf reject-relations ' \
              '--write-pbf %s' % (osmosis_cmd, pbf_file, key, value, output)
    elif osm == 'relations':
        cmd = '%s ' \
              '--read-pbf %s ' \
              '--tf accept-relations %s=%s ' \
              '--used-way ' \
              '--used-node ' \
              '--write-pbf %s' % (osmosis_cmd, pbf_file, key, value, output)
    print cmd
    call(cmd, shell=True)


def remove_pbf(pbf_file):
    print 'Remove %s' % pbf_file
    call('rm %s' % pbf_file, shell=True)


def merge(to_be_merged, continent):
    print 'Merge %s' % ' '.join(to_be_merged)
    output = '%s.pbf' % continent
    cmd = '%s ' % osmosis_cmd
    for one_file in to_be_merged:
        cmd += '--read-pbf %s ' % one_file

    cmd += '--merge ' * (len(to_be_merged) - 1)
    cmd += '--write-pbf %s' % output
    print cmd
    call(cmd, shell=True)
    return output


if __name__ == '__main__':

    for continent in continents:
        pbf_file = '%s-latest%s' % (continent, extension)
        download(continent)

        to_be_merged = []

        for osm in osm_types:
            for feature in features:
                key = feature[0]
                value = feature[1]
                output = '%s-%s-%s-%s.pbf' % (continent, key, value, osm)
                if (not exists(output) and not isfile(output)) or getsize(output) < 1000:
                    extract(key, value, osm, continent, output)
                to_be_merged.append(output)

        remove_pbf(pbf_file)

        output = merge(to_be_merged, continent)

        if isfile(output) and exists(output) and getsize(output) > 1000:
            for one_file in to_be_merged:
                remove_pbf(one_file)


# MERGE
# ../osmosis --read-pbf africa.pbf --read-pbf antarctica.pbf --read-pbf asia.pbf --read-pbf australia-oceania.pbf --read-pbf central-america.pbf --read-pbf europe.pbf --read-pbf north-america.pbf --read-pbf south-america.pbf --merge --merge --merge --merge --merge --merge --merge --write-pbf world.pbf
