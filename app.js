
(function () {
  var $ = function (s) { return document.getElementById(s) }
    , $ineed = $('ineed')
    , $ineedText = $('ineed_text')
    , $ineedSelect = $('ineed_select')
    , $results = $('results')
      // micro-templating
    , t = function (s, d){
        for (var p in d) s = s.replace(new RegExp('{' + p + '}', 'g'), d[p]);
        return s;
      }
    , render = function (results){
        var html = [], i = results.length, r, tags;
        while (i--) {
          if (!(r = results[i])._rendered) {
            tags = '<span>'+results[i].tags.join('</span> <span>')+'</span>';
            r.stat =
                '<div class="stat">'
              + (r.ghwatchers ? t('<a href="{ghurl}/stargazers" style="display: inline;"><span class="w icon">{ghwatchers}</span></a><a href="{ghurl}/network/members" style="display: inline;"><span class="f icon">{ghforks}</span></a>', r) : '')
              + (r.tweets ? t('<span class="t icon">{tweets}</span>', r) : '')
              + '</div>'
r.heading = 4; //r.name.length < 16 ? 3 : 4;
//					r._rendered = t('<li><a href="{url}"><div class="size">{size}</div><div class="title"><h{heading}>{name}</h{heading}>{stat}</div>{description}</a><div class="tags">'+tags+'</div></li>', r)
            r._rendered = t('<li><a href="https://masothue.com{url}"><div class="size">{conpany_active_date}</div><div class="title"><h{heading}>{conpany_tax}</h{heading}>{stat}</div>{company_name}</a><div class="tags">'+tags+'</div></li>', r)					
          }
          html.push(results[i]._rendered)
        }
        $results.innerHTML = html.join('');
        if(document.getElementById('tagVisibility').getAttribute('data-color') === 'true') {
          toggleColorMode();
        }
        var i, j, tagDivs, tagSpans, searchBox, libMatches, changeEvent;
        tagDivs = document.getElementsByClassName('tags');
        searchBox = document.getElementById('ineed_text');
        for(i = 0; i < tagDivs.length; i++) {
          if(tagDivs[i] !== undefined) {
            tagSpans = tagDivs[i].getElementsByTagName('span');
            for(j = 0; j < tagSpans.length; j++) {
              if(tagSpans[j] !== undefined) {
                tagSpans[j].onclick = function () {
                  searchBox.value = this.innerHTML;
                  window.location.hash = this.innerHTML;
                  changeEvent = document.createEvent("HTMLEvents");
                  changeEvent.initEvent("change", false, true);
                  searchBox.dispatchEvent(changeEvent);
                  window.scrollTo(0, 100);
                };
              }
            }
          }
        }
      }
  MicroJS.sort(function () { return 0.5 - Math.random() })

// mini feature-detect for some of the stuff we use with fallback for garbage browsers
;Array.prototype.forEach && Array.prototype.filter && document.documentElement.addEventListener && document.querySelector ?
(function () {
  // list of options to show in the pseudo-select box
  var options = [
          { tag: 'base', label: 'a base framework.' }
        , { tag: 'dom', label: 'a DOM utility.' }
        , { tag: 'templating', label: 'templating.' }
        , { tag: 'animation', label: 'CSS animation.' }
        , { tag: 'jsanimation', label: 'JavaScript animation.' }
        , { tag: 'css', label: 'a CSS selector engine.' }
        , { tag: 'data', label: 'data manipulation.' }
        , { tag: 'class', label: 'a Class system.' }
        , { tag: 'functional', label: 'functional programming.' }
        , { tag: 'loader', label: 'a JavaScript loader.' }
        , { tag: 'json', label: 'JSON.' }
        , { tag: 'ajax', label: 'AJAX.' }
        , { tag: 'testing', label: 'to test stuff (e.g. unit testing).' }
        , { tag: 'validation', label: 'to validate stuff.' }
        , { tag: 'games', label: 'to write a game.' }
        , { tag: 'canvas', label: 'to do CANVAS/2D graphics!' }
        , { tag: 'color', label: 'to convert colors.' }
        , { tag: 'list', label: 'to create searchable & sortable lists.' }
        , { tag: 'spa', label: 'single page apps.' }
        , { tag: 'storage', label: 'persistent storage.' }
        , { tag: 'mvc', label: 'client-side MVC.' }
        , { tag: 'feature', label: 'feature/browser detection.' }
        , { tag: 'events', label: 'events!' }
        , { tag: 'webkit', label: 'WebKit-specific libraries.' }
        , { tag: 'mobile', label: 'mobile-specific libraries.' }
        , { tag: 'responsive', label: 'libraries for responsive designs.' }
        , { tag: 'polyfill', label: 'polyfills.' }
        , { tag: 'analytics', label: 'analytics.' }
        , { tag: 'hyphenation', label: 'hyphenation.' }
        , { tag: 'async', label: 'asynchronous programming' }
        , { tag: 'compose', label: 'to compose my own framework!' }
        , { tag: 'micro', label: 'to code a site listing micro-frameworks!' }
      ]
    , selectBoxOptions = {
          itemHeight: 32 // how high is each item in the list?
        , maxItems: options.length // max items to show
        , minItems: 5 // min items to show
        , boxBorder: 2 // how many px is the border of the select box
      }
    , lastSearch
    , selectedItem = function () { return $ineedSelect.querySelector('div.selected') }
      // show drop-down box
    , showopt = function (opt) {
        if ($ineedSelect.style.display === '') return
        var s = '', height
        ;(opt || options).forEach(function (option) { s += '<div>' + option.label + '</div>' })
        $ineedSelect.innerHTML = s
        $ineedSelect.style.display = ''
        // how much space do we have to spare for the select box?
        height = roundToItemHeight(
            window.innerHeight - offsetTop($ineedSelect) + document.body.scrollTop + selectBoxOptions.boxBorder)
        // decide how big we should make the box
        height = Math.max(
            selectBoxOptions.itemHeight * selectBoxOptions.minItems
          , Math.min(selectBoxOptions.itemHeight * selectBoxOptions.maxItems, height))
        $ineedSelect.style.height = height + 'px'
      }
      // given x, round it to the nearest number of select box items we can fit in, - 1
    , roundToItemHeight = function (x) {
        return (Math.round(x / selectBoxOptions.itemHeight) - 1) * selectBoxOptions.itemHeight
      }
    , offsetTop = function (e) {
        var ot = 0
        while (e && e !== document) {
          ot += e.offsetTop
          e = e.offsetParent
        }
        return ot
      }
      // hide drop-down box
    , hideopt = function () {
        var si = selectedItem()
        if (si) si.className = ''
        $ineedSelect.style.display = 'none'
      }
      // here's a microlib right here, this little beauty is uber-helpful - @rvagg
      // delay invocation of arg1 by arg2 milliseconds, but push back that delay
      // each time we get another call before invocation, great for key-events
    , cumulativeDelayed = function() {
        var tid, args = Array.prototype.slice.call(arguments)
          , fn = args.shift(), timeout = args.shift()
        return function() {
          var _args = args.concat(Array.prototype.slice.call(arguments))
          if (tid) clearTimeout(tid)
          tid = setTimeout(function() { fn.apply(null, _args) }, timeout)
        }
      }
    , blurListener = cumulativeDelayed(function (e) { hideopt()}, 200)
    , focusListener = function (e) { showopt(); search() }
    , selectListener = function (e, el) { // click events
        if (e) el = e.target
        $ineedText.value = el.textContent || el.innerText
        e && keydownListener({ keyCode: 13 })
      }
    , keydownDelayed = cumulativeDelayed(function () { search() }, 250)
    , showsearch = function () {
        showopt();
        search();
      }
      // make our pseudo-select box work as if it was a real select box
    , keydownListener = function (e) {
        switch (e.keyCode) {
          case 38: //up
            showsearch();
            selectUp();
            break;
          case 40: //down
            showsearch();
            selectDown();
            break;
          case 13: //return
            hideopt();
            search();
            break;
          default:
            hideopt();
            keydownDelayed();
        }
      }
      // arrow-up
    , selectUp = function (e) {
        var si = selectedItem()
        if (si && si != $ineedSelect.firstChild) {
          si.className = ''
          ;(si = si.previousSibling).className = 'selected'
          if (si.offsetTop < $ineedSelect.scrollTop) $ineedSelect.scrollTop -= si.offsetHeight
          selectListener(null, si)
        }
      }
      // arrow-down
    , selectDown = function (e) {
        var si = selectedItem()
        if (!si) $ineedSelect.firstChild.className = 'selected'
        else if (si != $ineedSelect.lastChild) {
          si.className = ''
          ;(si = si.nextSibling).className = 'selected'
          if (si.offsetTop + si.offsetHeight > $ineedSelect.offsetHeight + $ineedSelect.scrollTop)
            $ineedSelect.scrollTop += si.offsetHeight
          selectListener(null, si)
        }
      }
    , search = cumulativeDelayed(function () {
        var i, libMatches, kw = $ineedText.value
        if (kw == lastSearch) return
        lastSearch = kw
        // special case for when text == an option, in which case search by tag
        for (i = 0; i < options.length; i++) {
          if (kw == options[i].label) { kw = options[i].tag; break; }
        }
        location.href = location.href.replace(/(#.*$)|($)/, '#' + (kw || ''))
        if (kw == 'micro') {
          $results.innerHTML = '<pre>' + $('scr').innerHTML
            .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
            .replace(/ /g, '&nbsp;').replace(/\n/g, '<br>') + '</pre>'
          return
        }
        kw = kw.split(/\s+/)
        libMatches = searchArray(MicroJS, kw)
        render(libMatches)
      }, 200)
    , searchArray = function (arr, kw) {
        if (!kw || !kw.length) return arr
        var kwre = [], l, i
        // turn keywords into matchers
        kw.forEach(function (k) { kwre.push(new RegExp(' [^ ]*' + k.replace(/[^\w\-\.]/g, '').toLowerCase() + '[^ ]* ')) })
        l = kwre.length
        // perform an AND search for all keywords
        return arr.filter(function (el) {
          for (i = 0; i < l; i++)
            if (!kwre[i].test(el._ss.toLowerCase())) return false
          return true
        })
      }

  // prepare the libs for search, make a search string that's space-separated with tags, name, description & url
  MicroJS.forEach(function (mj) { mj._ss = ' ' + mj.tags.concat([ mj.name, mj.description, mj.url, '' ]).join(' ') })

  $ineedText.addEventListener('focus', focusListener, false)
  $ineedText.addEventListener('click', focusListener, false)
  $ineedText.addEventListener('blur', blurListener, false)
  $ineedText.addEventListener('keydown', keydownListener, false)
  $ineedText.addEventListener('change', search, false)
  $ineedSelect.addEventListener('click', selectListener, false)

  ;(function(kw) {
    if (!kw) {
      return;
    }
    for (var i = 0; i < options.length; i++) {
      if (kw == options[i].tag) { kw = options[i].label; break; }
    }
    $ineedText.value = kw;
  }(location.href.split('#')[1]));

  search();
  $ineed.style.display = '';
  $ineedText.focus();
  window.setTimeout(hideopt,10);

})() : render(MicroJS); // fallback for old browsers, you don't deserve the sweetness!

})();

var toggleTagVisibility = function () {
  var tagStyleElement = document.getElementById('tagVisibility');
  if(tagStyleElement.innerHTML === '.tags{display:none;}') {
    tagStyleElement.innerHTML = '.tags{display:block;}';
  } else {
    tagStyleElement.innerHTML = '.tags{display:none;}';
  }
}

var toggleColorMode = function () {
  var sint, size, background, i, elements;
  elements = document.getElementById('results').children;
  if(elements[0].style.background === '') {
    for(i = 0; i < elements.length; i++) {
      size = elements[i].getElementsByClassName('size')[0].innerHTML;
      sint = (85+parseFloat(size)*60) > 360 ? 360 : 85+parseFloat(size)*60;
      background = 'background: #'+colorconv.HSL2HEX([sint,80,58])+';'
      + 'background: -webkit-gradient(linear, left top, left bottom, from(rgba(0,0,0,0.2)), color-stop(0.5, rgba(255,255,255,0.1)), color-stop(0.501, rgba(255,255,255,0.0)), to(rgba(255,255,255,0.0))), -webkit-gradient(linear, left top, left bottom, from(#'+colorconv.HSL2HEX([sint,80,58])+'), to(#'+colorconv.HSL2HEX([sint,60,40])+'));'
      + 'background: -webkit-linear-gradient(rgba(0,0,0,0.2), rgba(255,255,255,0.1) 50%, rgba(255,255,255,0) 50.01%, rgba(255,255,255,0)), -webkit-linear-gradient(#'+colorconv.HSL2HEX([sint,80,58])+', #'+colorconv.HSL2HEX([sint,60,40])+');'
      + 'background: -moz-linear-gradient(rgba(0,0,0,0.2), rgba(255,255,255,0.1) 50%, rgba(255,255,255,0) 50.01%, rgba(255,255,255,0)), -moz-linear-gradient(#'+colorconv.HSL2HEX([sint,80,58])+', #'+colorconv.HSL2HEX([sint,60,40])+');'
      + 'background: -ms-linear-gradient(rgba(0,0,0,0.2), rgba(255,255,255,0.1) 50%, rgba(255,255,255,0) 50.01%, rgba(255,255,255,0)), -ms-linear-gradient(#'+colorconv.HSL2HEX([sint,80,58])+', #'+colorconv.HSL2HEX([sint,60,40])+');'
      + 'background: -o-linear-gradient(rgba(0,0,0,0.2), rgba(255,255,255,0.1) 50%, rgba(255,255,255,0) 50.01%, rgba(255,255,255,0)), -o-linear-gradient(#'+colorconv.HSL2HEX([sint,80,58])+', #'+colorconv.HSL2HEX([sint,60,40])+');'
      + 'background: linear-gradient(rgba(0,0,0,0.2), rgba(255,255,255,0.1) 50%, rgba(255,255,255,0) 50.01%, rgba(255,255,255,0)), linear-gradient(#'+colorconv.HSL2HEX([sint,80,58])+', #'+colorconv.HSL2HEX([sint,60,40])+');';
      elements[i].setAttribute("style", background);
    }
    document.getElementById('tagVisibility').setAttribute('data-color',true);
  } else {
    for(i = 0; i < elements.length; i++) {
      elements[i].style.background = '';
      document.getElementById('tagVisibility').setAttribute('data-color',false);
    }
  }
}
