__title__ = "Search 'The Prompt' show notes"
__author__ = "Fernando Xavier de Freitas Crespo"
__author_email__ = "fernando@crespo.in"
__version__ = "1.0"

require "uri"
require "open-uri"
require "hpricot"
require "yaml"

query = "{query}"

item_template='  <item arg="{0}" valid="{3}" autocomplete="{0}"><title><![CDATA[{1}]]></title><subtitle><![CDATA[{2}]]></subtitle><icon>icon.png</icon></item>'

cache = {}

def template(episode)
    return "  <item arg=\"#{episode[:episode]}\" valid=\"yes\" autocomplete=\"#{episode[:episode]}\"><title><![CDATA[#{episode[:title]}]]></title><subtitle><![CDATA[#{episode[:subtitle]}]]></subtitle><icon>icon.png</icon></item>"
end

def get_episodes_in_page(page)
    episodes = []
    result = URI.parse("http://5by5.tv/prompt/page/#{page}").read
    doc = Hpricot(result)

    doc.search("div[@class='episode'")
    
    (doc/"div[@class='episode']").each do |div|
        title = (div/"h3/a").inner_html.strip
        episode_number = /.*#(?<number>[0-9]{,3}).*/.match(title)[:number]
        title.gsub!(/#(?<number>[0-9]{,3}): /, "")
        subtitle = (div/"p").inner_html.strip
        episodes << {:episode => episode_number, :title => title, :subtitle => subtitle}
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
    for i in 1..20 # Pick last 20 pages to cache all episodes
        episodes_in_page_i = get_episodes_in_page(i)
        for episode in episodes_in_page_i
            #puts("Caching episode #{episode[:episode]}")
            add_episode_to_cache(cache, episode)
        end
    end
end
#puts get_episodes_in_page(1)

cache_all(cache)

#puts template(get_episodes_in_page(1)[0])

serialized = cache.sort.to_yaml

File.open("#{`echo $HOME`.strip}/teste.yaml", "w") { |file| file.write(serialized) }