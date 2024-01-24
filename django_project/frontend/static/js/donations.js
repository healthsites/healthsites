function scrape(
  $element, url, defaultTitle, defaultIcon
) {
  fetch(url)
    .then(response => response.text())
    .then((response) => {
      const parser = new DOMParser()
      const htmlDoc = parser.parseFromString(response, 'text/html')
      if (!defaultTitle) {
        let title = htmlDoc.getElementsByClassName('p-campaign-title')[0].innerText
        if (title) {
          $element.find('.desc').append(title)
        }
      }
      if (!defaultIcon) {
        let icon = htmlDoc.getElementsByClassName('p-campaign-collage')[0]
        if (icon) {
          $element.find('.icon').append(icon)
        }
      }
    })
}

function renderCampaigns($element, data) {
  data.map(
    row => {
      const id = `campaign-${row.id}`;
      let platform = ''
      if (row.url.includes('gofundme')) {
        platform = '<img class="platform" src="/static/img/donation/gofundme.svg"/>'
      }
      $element.append(`
        <a href="${row.url}" target="_blank" id="${id}">
            <div class="icon">   
                ${row.icon ? "<img src='" + row.icon + "'>" : ''}             
            </div>
            <div class="desc">
                ${platform}
                ${row.title ? row.title : ''}
            </div>
        </a>      
      `)
      if (row.url.includes('gofundme')) {
        scrape($('#' + id), row.url, row.title, row.icon)
      }
    }
  )
}