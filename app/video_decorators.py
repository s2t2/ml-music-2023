

from pytube import YouTube
# for pytube video objects


def video_metadata(video:YouTube):
    return {

        'video_id': video.video_id,
        'channel_id': video.channel_id,
        'author': video.author,

        'title': video.title,
        'description': video.description,

        'keywords': video.keywords,
        'length': video.length,
        'publish_date': video.publish_date,
        'rating': video.rating,
        'views': video.views,

        'channel_url': video.channel_url,
        'thumbnail_url': video.thumbnail_url,
        'watch_url': video.watch_url,

        #'caption_tracks': video.caption_tracks,
        #'captions': video.captions,

        #'age_restricted': video.age_restricted,
        #'allow_oauth_cache': video.allow_oauth_cache,
        #'bypass_age_gate': video.bypass_age_gate,
        #'check_availability': video.check_availability,
        #'embed_html': video.embed_html,
        #'embed_url': video.embed_url,
        #'fmt_streams': video.fmt_streams,
        #'from_id': video.from_id,
        #'initial_data': video.initial_data,
        #'js': video.js,
        #'js_url': video.js_url,
        #'metadata': video.metadata,
        #'register_on_complete_callback': video.register_on_complete_callback,
        #'register_on_progress_callback': video.register_on_progress_callback,
        #'stream_monostate': video.stream_monostate,
        #'streaming_data': video.streaming_data,
        #'streams': video.streams,
        #'use_oauth': video.use_oauth,
        #'watch_html': video.watch_html,
        #'vid_info': video.vid_info,
    }
