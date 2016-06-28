
import yaml
import os
import re
import csv
from shutil import copyfile


class NewMultitrack(object):
    """ Class to populate new Multitrack
    """
    def __init__(self, save_path):
        self.artist = ''
        self.title = ''
        self.album = ''
        self.composer = ''
        self.producer = ''
        self.genre = ''
        self.website = ''
        self.excerpt = ''
        self.has_bleed = ''
        self.instrumental = ''
        self.origin = ''
        self.mix_filename = ''
        self.stem_dir = ''
        self.raw_dir = ''
        self.stem_info = {}
        self.raw_info = {}
        self.ranking = []
        self.stem_fchange_dict = {}

        self._init_metadata()

        self.stem_keys = ['filename', 'instrument', 'component', 'raw']
        self.raw_keys = ['filename', 'instrument']

        self.save_path = save_path
        self.track_dirname = ''
        self.track_path = ''

        self.metadata_fname = ''
        self.metadata_path = ''

        self.mix_path = ''

        self.stem_dir = ''
        self.stem_path = ''
        self.raw_dir = ''
        self.raw_path = ''
        self.annot_dir = ''
        self.pitch_dir = ''
        self.mel_ranking = ''
        self.annot_path = ''
        self.pitch_path = ''
        self.ranking_path = ''

        self.meta_fmt = "%s_METADATA.yaml"
        self.stem_dir_fmt = "%s_STEMS"
        self.raw_dir_fmt = "%s_RAW"
        self.mix_fmt = "%s_MIX.wav"
        self.annot_dir_fmt = "%s_ANNOTATIONS"
        self.pitch_dir_fmt = "%s_PITCH"
        self.mel_ranking_fmt = "%s_RANKING.txt"

        self.stem_fmt = ''
        self.raw_fmt = ''

        self.track_id = ''

    def _init_metadata(self):
        # initialize metadata dictionary
        keys = ['artist', 'title', 'album', 'composer', 'producer',
                'genre', 'website', 'excerpt', 'has_bleed', 'instrumental',
                'origin', 'mix_filename', 'stem_dir', 'raw_dir', 'stems',
                'release date']
        self.metadata_dict = dict.fromkeys(keys)
        self.metadata_dict['stems'] = {}

    def setArtist(self, artist):
        self.artist = artist
        if self.title:
            self._setTrackID()

    def setTitle(self, title):
        self.title = title
        if self.artist:
            self._setTrackID()

    def setAlbum(self, album):
        self.album = album

    def setComposer(self, composer):
        self.composer = composer

    def setProducer(self, producer):
        self.producer = producer

    def setGenre(self, genre):
        self.genre = genre

    def setWebsite(self, website):
        self.website = website

    def setExcerpt(self, excerpt):
        self.excerpt = excerpt

    def setHasBleed(self, has_bleed):
        self.has_bleed = has_bleed

    def setInstrumental(self, instrumental):
        self.instrumental = instrumental

    def setOrigin(self, origin):
        self.origin = origin

    def setRanking(self, ranking):
        self.ranking = ranking

    def _setTrackID(self):
        artist = self.artist
        title = self.title
        artist_camel = re.sub(r'\W+', '', artist.replace("'", '').title())
        title_camel = re.sub(r'\W+', '', title.replace("'", '').title())
        self.track_id = "%s_%s" % (artist_camel, title_camel)
        self._setFilenames()

    def _setFilenames(self):
        self.metadata_fname = self.meta_fmt % self.track_id
        self.mix_filename = self.mix_fmt % self.track_id
        self.stem_dir = self.stem_dir_fmt % self.track_id
        self.raw_dir = self.raw_dir_fmt % self.track_id
        self.stem_fmt = "%s_STEM_%%s.wav" % self.track_id
        self.raw_fmt = "%s_RAW_%%s_%%s.wav" % self.track_id
        self.annot_dir = self.annot_dir_fmt % self.track_id
        self.pitch_dir = self.pitch_dir_fmt % self.track_id
        self.mel_ranking = self.mel_ranking_fmt % self.track_id

        self.track_dirname = self.track_id
        self.track_path = os.path.join(self.save_path, self.track_dirname)
        self._setFilepaths()

    def _setFilepaths(self):
        self.metadata_path = os.path.join(self.track_path, self.metadata_fname)
        self.mix_path = os.path.join(self.track_path, self.mix_filename)
        self.stem_path = os.path.join(self.track_path, self.stem_dir)
        self.raw_path = os.path.join(self.track_path, self.raw_dir)
        self.annot_path = os.path.join(self.track_path, self.annot_dir)
        self.pitch_path = os.path.join(self.annot_path, self.pitch_dir)
        self.ranking_path = os.path.join(self.annot_path, self.mel_ranking)

    def makeFileStructure(self):
        if not os.path.exists(self.track_path):
            os.mkdir(self.track_path)

        if not os.path.exists(self.stem_path):
            os.mkdir(self.stem_path)

        if not os.path.exists(self.raw_path):
            os.mkdir(self.raw_path)

        if not os.path.exists(self.annot_path):
            os.mkdir(self.annot_path)

        if not os.path.exists(self.pitch_path):
            os.mkdir(self.pitch_path)

    def fillMetadata(self):
        self.metadata_dict['artist'] = self.artist
        self.metadata_dict['title'] = self.title
        self.metadata_dict['album'] = self.album
        self.metadata_dict['composer'] = self.composer
        self.metadata_dict['producer'] = self.producer
        self.metadata_dict['genre'] = self.genre
        self.metadata_dict['website'] = self.website
        self.metadata_dict['excerpt'] = self.excerpt
        self.metadata_dict['has_bleed'] = self.has_bleed
        self.metadata_dict['instrumental'] = self.instrumental
        self.metadata_dict['origin'] = self.origin
        self.metadata_dict['mix_filename'] = self.mix_filename
        self.metadata_dict['stem_dir'] = self.stem_dir
        self.metadata_dict['raw_dir'] = self.raw_dir

    def addMixFile(self, fpath):
        copyfile(fpath, self.mix_path)

    def addStemFile(self, fpath, instrument, component):
        stem_idx = int(len(self.metadata_dict['stems'].keys()) + 1)

        new_fname = self.stem_fmt % ("%02d" % stem_idx)
        new_fpath = os.path.join(self.stem_path, new_fname)

        copyfile(fpath, new_fpath)
        self.stem_fchange_dict[os.path.basename(fpath)] = \
            os.path.basename(new_fpath)

        temp_dict = dict.fromkeys(self.stem_keys)
        temp_dict['filename'] = self.stem_fmt % ("%02d" % stem_idx)
        temp_dict['instrument'] = instrument
        temp_dict['component'] = component
        temp_dict['raw'] = {}

        self.metadata_dict['stems']["S%02d" % stem_idx] = temp_dict
        return stem_idx

    def addRawFile(self, fpath, stem_idx, instrument):

        stem_str = "S%02d" % stem_idx

        # get next source index
        raw_idx = len(self.metadata_dict['stems'][stem_str]['raw'].keys()) + 1
        raw_str = "R%02d" % raw_idx

        # define output filename and path
        new_fname = self.raw_fmt % (("%02d" % stem_idx), ("%02d" % raw_idx))
        new_fpath = os.path.join(self.raw_path, new_fname)

        # copy source file to source directory
        copyfile(fpath, new_fpath)

        # add metadata to dictionary
        # Ensure that stem exists
        assert stem_str in self.metadata_dict['stems'].keys(), \
            "Stem index %s does not exist" % stem_str

        # fill dictionary #
        temp_dict = dict.fromkeys(self.raw_keys)
        temp_dict['filename'] = self.raw_fmt % (("%02d" % stem_idx), ("%02d" % raw_idx))
        temp_dict['instrument'] = instrument
        self.metadata_dict['stems'][stem_str]['raw'][raw_str] = temp_dict

    def writeMetadataFile(self):
        f_out = open(self.metadata_path, 'w')
        yaml.dump(self.metadata_dict, f_out,
                  indent=2, default_flow_style=False)
        f_out.close()

    def writeRankingFile(self):
        with open(self.ranking_path, 'w') as fhandle:
            writer = csv.writer(fhandle)
            writer.writerows(self.ranking)


def get_dict_leaves(dictionary):
    vals = []
    if type(dictionary) == dict:
        keys = dictionary.keys()
        for k in keys:
            if type(dictionary[k]) == dict:
                for v in get_dict_leaves(dictionary[k]):
                    vals.append(v)
            else:
                for v in dictionary[k]:
                    vals.append(v)
    else:
        for v in dictionary:
            vals.append(v)

    vals = set(vals)
    return vals
