document.addEventListener("DOMContentLoaded", () => {
  const grid = document.getElementById("itemsGrid");
  const search = document.getElementById("searchInput");
  const sort = document.getElementById("sortSelect");
  let items = [];
  let activeStatus = "all";
  let viewMode = "grid";
  let initialRandom = true;

  const esc = s => String(s ?? "").replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const initials = name => (name || "CU").split(/\s+/).slice(0,2).map(x=>x[0]).join("").toUpperCase();
  const selected = type => [...document.querySelectorAll(`[data-filter="${type}"]:checked`)].map(x=>x.value.toLowerCase());

  async function loadItems(){
    const r = await fetch("/api/items");
    items = await r.json();
    render();
  }

  function matches(item){
    const q = search.value.trim().toLowerCase();
    const cat = selected("category"), dep = selected("department"), col = selected("color"), loc = selected("location");
    const text = `${item.title} ${item.category} ${item.department||""} ${item.location||""} ${item.description||""}`.toLowerCase();
    return (activeStatus === "all" || item.item_type === activeStatus)
      && (!cat.length || cat.includes((item.category||"").toLowerCase()))
      && (!dep.length || dep.includes((item.department||"").toLowerCase()))
      && (!col.length || col.includes((item.color||"").toLowerCase()))
      && (!loc.length || loc.includes((item.location||"").toLowerCase()))
      && (!q || text.includes(q));
  }

  function render(){
    let visible = items.filter(matches);
    if(!initialRandom){
      if(sort.value === "oldest") visible.sort((a,b)=>a.created_at.localeCompare(b.created_at));
      if(sort.value === "newest") visible.sort((a,b)=>b.created_at.localeCompare(a.created_at));
    }
    if(sort.value === "az") visible.sort((a,b)=>a.title.localeCompare(b.title));

    document.getElementById("showingText").textContent = `Showing ${visible.length} item${visible.length===1?"":"s"}`;
    document.querySelectorAll("[data-count-for]").forEach(el => {
      const val = el.dataset.countFor.toLowerCase();
      el.textContent = items.filter(i => i.category.toLowerCase() === val).length;
    });

    if(!visible.length){
      grid.innerHTML = `<div class="empty"><div style="font-size:40px">⌕</div><h3>No matching items</h3><p>Try changing your search or filters.</p><button class="primary-btn" id="emptyReport">Report Item</button></div>`;
      document.getElementById("emptyReport").onclick = () => openModal("reportModal");
      return;
    }

    grid.innerHTML = visible.map(item => `
      <article class="card">
        <div class="card-image">
          <span class="tag ${item.item_type}">${item.item_type.toUpperCase()}</span>
          <button class="heart ${item.is_favorite ? "active":""}" data-fav="${item.id}" title="Save item">${item.is_favorite ? "♥":"♡"}</button>
          ${item.image ? `<img src="/static/uploads/${encodeURIComponent(item.image)}" alt="${esc(item.title)}">` : `<div class="placeholder">${item.item_type==="lost"?"🔎":"🎒"}</div>`}
        </div>
        <div class="card-body">
          <h3>${esc(item.title)}</h3>
          <div class="sub">${esc(item.category)}</div>
          <div class="meta"><span>⌖ ${esc(item.location || "Campus location not specified")}</span><span>◷ ${timeAgo(item.created_at)}</span></div>
          <div class="chips"><span class="chip">${esc(item.category)}</span>${item.color ? `<span class="chip color">${esc(item.color)}</span>`:""}</div>
          <div class="card-foot"><div class="poster"><span class="mini-avatar">${initials(item.poster_name)}</span><span>By ${esc(item.poster_name)}</span></div><button class="details" data-detail="${item.id}">Details →</button></div>
        </div>
      </article>`).join("");

    grid.querySelectorAll("[data-detail]").forEach(b => b.onclick=()=>showDetail(Number(b.dataset.detail)));
    grid.querySelectorAll("[data-fav]").forEach(b => b.onclick=async e=>{
      e.stopPropagation();
      const r=await fetch(`/api/items/${b.dataset.fav}/favorite`,{method:"POST"});
      const data=await r.json();
      const it=items.find(x=>x.id==b.dataset.fav); if(it){it.is_favorite=data.favorite; render();}
    });
  }

  function timeAgo(date){
    const diff = Math.max(0, Date.now()-new Date(date).getTime());
    const mins=Math.floor(diff/60000), hrs=Math.floor(mins/60), days=Math.floor(hrs/24);
    if(mins<1)return"just now"; if(mins<60)return`${mins} min ago`; if(hrs<24)return`${hrs} hour${hrs>1?"s":""} ago`; return`${days} day${days>1?"s":""} ago`;
  }

  function openModal(id){document.getElementById(id).classList.add("show");document.body.style.overflow="hidden";}
  function closeModal(id){document.getElementById(id).classList.remove("show");if(!document.querySelector(".modal.show"))document.body.style.overflow="";}

  async function showDetail(id){
    const item=items.find(x=>x.id===id); if(!item)return;
    const image=item.image?`<img src="/static/uploads/${encodeURIComponent(item.image)}" alt="${esc(item.title)}">`:`<div class="placeholder" style="height:100%">🔎</div>`;
    document.getElementById("detailContent").innerHTML=`
      <div class="detail-layout"><div class="detail-image">${image}</div><div class="detail-info">
      <span class="tag ${item.item_type}" style="position:static;display:inline-block">${item.item_type.toUpperCase()}</span>
      <h2>${esc(item.title)}</h2><p class="muted">${esc(item.description||"No description provided.")}</p>
      <div class="info-grid"><div class="info"><small>Category</small><b>${esc(item.category)}</b></div><div class="info"><small>Department</small><b>${esc(item.department||"-")}</b></div><div class="info"><small>Color</small><b>${esc(item.color||"-")}</b></div><div class="info"><small>Location</small><b>${esc(item.location||"-")}</b></div></div>
      <div style="margin-top:16px"><small>Posted by</small><div style="font-weight:800;margin-top:5px">${esc(item.poster_name)}</div><div style="font-size:11px;color:#697391;margin-top:3px">${esc(item.poster_email)}</div></div>
      <div class="contact-row"><a class="contact call" href="${item.poster_phone?`tel:${esc(item.poster_phone)}`:"#"}">☎ Call</a><a class="contact wa" target="_blank" href="${item.poster_phone?`https://wa.me/${item.poster_phone.replace(/\\D/g,"")}`:"#"}">WhatsApp</a></div>
      </div></div>`;
    openModal("detailModal");
  }

  document.querySelectorAll(".status-pill,.big-status-btn").forEach(btn=>btn.onclick=()=>{
    activeStatus=btn.dataset.status;
    initialRandom=false;
    document.querySelectorAll("[data-status]").forEach(b=>b.classList.toggle("active",b.dataset.status===activeStatus));
    render();
  });
  document.querySelectorAll("[data-filter]").forEach(x=>x.onchange=()=>{initialRandom=false;render();});
  search.oninput=()=>{initialRandom=false;render();}; sort.onchange=()=>{initialRandom=false;render();};
  document.getElementById("clearAll").onclick=()=>{document.querySelectorAll("[data-filter]").forEach(x=>x.checked=false);search.value="";activeStatus="all";document.querySelectorAll("[data-status]").forEach(b=>b.classList.toggle("active",b.dataset.status==="all"));render();};
  document.querySelectorAll("[data-toggle]").forEach(b=>b.onclick=()=>{const el=document.getElementById(b.dataset.toggle);el.style.display=el.style.display==="none"?"grid":"none";});

  document.querySelectorAll("[data-close]").forEach(b=>b.onclick=()=>closeModal(b.dataset.close));
  document.querySelectorAll(".modal").forEach(m=>m.onclick=e=>{if(e.target===m)closeModal(m.id);});
  document.addEventListener("keydown",e=>{if(e.key==="Escape")document.querySelectorAll(".modal.show").forEach(m=>closeModal(m.id));});

  document.querySelectorAll(".type-btn").forEach(b=>b.onclick=()=>{document.querySelectorAll(".type-btn").forEach(x=>x.classList.remove("active"));b.classList.add("active");document.getElementById("itemType").value=b.dataset.type;});
  document.getElementById("openReport").onclick=()=>openModal("reportModal");
  document.getElementById("helpReport").onclick=()=>openModal("reportModal");

  document.getElementById("reportForm").onsubmit=async e=>{
    e.preventDefault();
    const btn=e.submitter;btn.disabled=true;btn.textContent="Publishing...";
    try{
      const r=await fetch("/api/items",{method:"POST",body:new FormData(e.target)});
      const data=await r.json();
      if(!r.ok)throw new Error(data.error||"Unable to publish");
      e.target.reset();document.querySelectorAll(".type-btn").forEach(x=>x.classList.remove("active"));document.querySelector('.type-btn[data-type="lost"]').classList.add("active");document.getElementById("itemType").value="lost";closeModal("reportModal");await loadItems();alert("Item published successfully.");
    }catch(err){alert(err.message)}finally{btn.disabled=false;btn.textContent="Publish Item";}
  };

  document.getElementById("profileBtn").onclick=e=>{e.stopPropagation();document.getElementById("profileMenu").classList.toggle("show");document.getElementById("notificationPanel").classList.remove("show");};
  document.getElementById("bellBtn").onclick=async e=>{e.stopPropagation();document.getElementById("notificationPanel").classList.toggle("show");document.getElementById("profileMenu").classList.remove("show");await loadNotifications();};
  document.addEventListener("click",()=>{document.getElementById("profileMenu").classList.remove("show");document.getElementById("notificationPanel").classList.remove("show");});
  document.getElementById("profileMenu").onclick=e=>e.stopPropagation();document.getElementById("notificationPanel").onclick=e=>e.stopPropagation();

  document.getElementById("editProfile").onclick=()=>{document.getElementById("profileMenu").classList.remove("show");openModal("profileModal");};
  document.getElementById("myItems").onclick=async()=>{document.getElementById("profileMenu").classList.remove("show");const r=await fetch("/api/my-items");const mine=await r.json();alert(mine.length?mine.map(x=>`${x.item_type.toUpperCase()} • ${x.title}`).join("\n"):"You have not posted any reports yet.");};

  document.getElementById("profileForm").onsubmit=async e=>{
    e.preventDefault();const r=await fetch("/api/profile",{method:"POST",body:new FormData(e.target)});const data=await r.json();if(!r.ok){alert(data.error);return;}alert("Profile updated.");location.reload();
  };

  async function loadNotifications(){
    const r=await fetch("/api/notifications");const data=await r.json();
    document.getElementById("noticeCount").textContent=data.unread;
    document.getElementById("notificationList").innerHTML=data.items.length?data.items.map(n=>`<div class="notice"><b>${esc(n.title)}</b><span>${esc(n.message)}</span></div>`).join(""):`<div class="notice"><span>No new notifications.</span></div>`;
    if(data.unread) await fetch("/api/notifications/read",{method:"POST"});
  }
  setInterval(loadNotifications,30000);

  document.getElementById("gridView").onclick=()=>{viewMode="grid";grid.style.gridTemplateColumns="repeat(4,minmax(0,1fr))";};
  document.getElementById("listView").onclick=()=>{viewMode="list";grid.style.gridTemplateColumns="1fr";};
  loadItems();loadNotifications();
});
