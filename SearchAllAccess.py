import common
import time
import sys

if len(sys.argv) < 3:
    common.log('ERROR input and output file are required')
    time.sleep(3)
    exit()

inputfile = sys.argv[1]
outputfile = sys.argv[2]

out = open(outputfile, 'w')
with open(inputfile, 'r') as f:
    api = common.open_api()
    for line in f:
        fields = line.strip().split('\t')
        input_artist = fields[0]
        input_album = fields[1]
        input_year = fields[2]
        input_tracks = int(fields[3])

        results = api.search_all_access(input_album)

        out.write('\n')
        out.write('==========\n')
        print "Checking '%s' by '%s' from %s with %s tracks..." % (input_album, input_artist, input_year, input_tracks),
        out.write("Checking '%s' by '%s' from %s with %s tracks\n" % (input_album, input_artist, input_year, input_tracks))

        hits = 0
        total_album_hits = len(results['album_hits'])
        for album in results['album_hits']:
            name = album['album']['name']
            artist = album['album']['albumArtist']
            album_id = album['album']['albumId']
            if name.startswith(input_album) and input_artist == artist:
                hits += 1
                aresults = api.get_album_info(album_id)
                found_sym = '-'
                tracks = 'unknown'
                year = 'unknown'
                if aresults:
                    if aresults.has_key('tracks'):
                        tracks = len(aresults['tracks'])
                        if tracks >= input_tracks:
                            found_sym = '*'
                    if aresults.has_key('year'):
                        year = aresults['year']
                out.write("   %s ALBUM: %s  ARTIST: %s  YEAR: %s  TRACKS: %s\n" % (found_sym,
                                                                                   name.encode('utf-8'),
                                                                                   artist.encode('utf-8'),
                                                                                   year,
                                                                                   tracks))
        print "%s hits (%s total album hits)" % (hits, total_album_hits)

    common.close_api()
out.close()
