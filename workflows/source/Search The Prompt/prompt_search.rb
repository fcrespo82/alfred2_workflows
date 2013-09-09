#!/usr/bin/ruby
# encoding: UTF-8

__title__ = "Search 'The Prompt' show notes"
__author__ = "Fernando Xavier de Freitas Crespo"
__author_email__ = "fernando@crespo.in"
__version__ = "1.0"

require "uri"
require "open-uri"
require "hpricot"
require "yaml"

$query = "a"

def template(episode, valid)
    return "  <item arg=\"#{episode[:episode]}\" valid=\"#{valid}\" autocomplete=\"#{episode[:episode]}\"><title><![CDATA[#{episode[:title]}]]></title><subtitle><![CDATA[#{episode[:subtitle]}]]></subtitle><icon>icon.png</icon></item>\n"
end

def get_episodes_in_page(page)
    episodes = []
    result = URI.parse("http://5by5.tv/prompt/page/#{page}").read
    doc = Hpricot(result)
    (doc/"div[@class='episode']").each do |div|
        title = (div/"h3/a").inner_html.strip
        episode_number = title[1..title.index(':')-1]
        subtitle = (div/"p").inner_html.strip
        episodes << {episode: episode_number, title: title, subtitle: subtitle}
    end
    return episodes
end

def add_episode_to_cache(cache, episode)
    episode_number = episode[:episode].rjust(4, '0')
    if not cache.keys.include?(episode_number)
        cache[episode_number] = episode
        return true
    end
    return false
end

def cache_all(cache)
    for i in 1..3 # Pick last 3 pages to cache all episodes
        episodes_in_page_i = get_episodes_in_page(i)
        for episode in episodes_in_page_i
            add_episode_to_cache(cache, episode)
        end
    end
end

def list_all(cache)
    all = ""
    for episode in cache.sort
        all += template(episode[1]) + "\n"
    end
    return all
end

def log(text)
    File.open("log.txt", "a") { |file| file.write(text + "\n") }
end

def save_cache(cache)
    File.open("cache.yaml", "w") { |file| file.write(cache.to_yaml) }
end

def load_cache
    begin
        result = YAML.load_file("cache.yaml")
    rescue Exception => e
        result = nil
    end
    return result
end

def main
    cached_items = load_cache

    if not cached_items
        cached_items = {}
        cache_all(cached_items)
    end

    result = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<items>\n"
    if cached_items
        # Force get lastest 10 episodes (first page) to keep up to date
        episodes_in_page_1 = get_episodes_in_page(1)
        for episode in episodes_in_page_1
            add_episode_to_cache(cached_items, episode)
        end

        for episode_number in cached_items.keys.sort.reverse
            search_in = cached_items[episode_number][:episode].downcase + " "
            search_in += cached_items[episode_number][:title].downcase + " "
            search_in += cached_items[episode_number][:subtitle].downcase
            if search_in.include?($query.downcase)
                result += template(cached_items[episode_number], "yes")
            end
        end

    else
        result += template({episode: 0, title: "Error", subtitle: "Could not read cache file"}, "no")
    end
    result += "</items>"
    
    return result, cached_items
end

text, items = main
save_cache(items)
puts text