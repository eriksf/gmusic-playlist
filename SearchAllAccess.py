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
        artist_name = fields[0]
        album_name = fields[1]

        results = api.search_all_access(album_name)

        print ''
        print '=========='
        print 'Checking %s by %s' % (album_name, artist_name)

        for album in results['album_hits']:
            name = album['album']['name']
            artist = album['album']['albumArtist']
            album_id = album['album']['albumId']
            if name.startswith(album_name) and artist_name == artist:
                aresults = api.get_album_info(album_id)
                if aresults:
                    tracks = len(aresults['tracks'])
                    print "   * Album: %s  Artist: %s  Tracks: %s" % (name, artist, tracks)
                else:
                    print "   * Album: %s  Artist: %s  Tracks: unknown" % (name, artist)

    common.close_api()
