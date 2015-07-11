import common
import time
import sys

if len(sys.argv) < 2:
    common.log('ERROR input file is required')
    time.sleep(3)
    exit()

inputfile = sys.argv[1]

with open(inputfile, 'r') as f:
    api = common.open_api()
    for line in f:
        fields = line.strip().split('\t')
        input_artist = fields[0]
        input_album = fields[1]
        input_year = fields[2]
        input_tracks = int(fields[3])

        results = api.search_all_access(input_album)

        print ''
        print '=========='
        print "Checking '%s' by '%s' from %s with %s tracks" % (input_album, input_artist, input_year, input_tracks)

        for album in results['album_hits']:
            name = album['album']['name']
            artist = album['album']['albumArtist']
            album_id = album['album']['albumId']
            if name.startswith(input_album) and input_artist == artist:
                aresults = api.get_album_info(album_id)
                if aresults:
                    tracks = len(aresults['tracks'])
                    year = aresults['year']
                    if tracks >= input_tracks:
                        print "   * ALBUM: %s  ARTIST: %s  YEAR: %s  TRACKS: %s" % (name, artist, year, tracks)
                    else:
                        print "   - ALBUM: %s  ARTIST: %s  YEAR: %s  TRACKS: %s" % (name, artist, year, tracks)
                else:
                    print "   * ALBUM: %s  ARTIST: %s  YEAR: unknown  TRACKS: unknown" % (name, artist)

    common.close_api()
