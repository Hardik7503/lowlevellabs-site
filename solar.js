(() => {
  const worlds = {
    boot:{title:"Boot & Firmware",kicker:"WORLD 01 · BOOT PATH",description:"Follow the journey from reset and firmware initialization to the operating system.",articles:[["BIOS vs. UEFI","articles/bios-vs-uefi.html"],["MBR vs. GPT: How Bootloaders Start","articles/mbr-vs-gpt-bootloader.html"],["From Reset Vector to Kernel Entry","articles/bootloader-to-kernel-handoff.html"]]},
    arch:{title:"Processor Architecture",kicker:"WORLD 02 · CPU DESIGN",description:"Explore instruction sets, cache behavior, and the architecture underneath software.",articles:[["Armv7-A vs. Armv8-A: AArch32 and AArch64","articles/armv7-vs-armv8-aarch64.html"],["MESI Cache Coherence Explained","articles/cache-coherence-mesi.html"],["DMA and Cache Coherency","articles/dma-cache-coherency.html"]]},
    os:{title:"Operating Systems",kicker:"WORLD 03 · OS INTERNALS",description:"Understand the kernel's responsibilities and how hardware becomes usable software.",articles:[["What Happens When a Linux Driver Probes?","articles/linux-driver-probe.html"],["Device Tree: How Linux Describes Hardware","articles/device-tree-driver-binding.html"],["Process Context vs. Hard IRQ Context","articles/interrupt-context-vs-process-context.html"]]},
    drivers:{title:"Linux Device Drivers",kicker:"WORLD 04 · DRIVER ENGINEERING",description:"From bus matching to character devices, learn how kernel code exposes hardware.",articles:[["Platform, I²C, and SPI Drivers","articles/linux-platform-i2c-spi-drivers.html"],["From open() to read(): Character Drivers","articles/linux-character-device-read-write.html"],["Designing a Robust ioctl Interface","articles/ioctl-abi-design.html"]]},
    memory:{title:"Memory & Storage",kicker:"WORLD 05 · DATA PATHS",description:"Trace how data moves through caches, RAM, DMA engines, and non-volatile storage.",articles:[["DMA and Cache Coherency","articles/dma-cache-coherency.html"],["NOR vs. NAND Flash","articles/nor-vs-nand.html"],["MESI Cache Coherence Explained","articles/cache-coherence-mesi.html"]]},
    multi:{title:"Multicore Systems",kicker:"WORLD 06 · COORDINATION",description:"Explore how cores communicate, share state, and reason about concurrency.",articles:[["SMP Communication: IPIs and Shared Memory","articles/smp-interprocessor-interrupt-mailbox.html"],["MESI Cache Coherence Explained","articles/cache-coherence-mesi.html"],["DMA and Cache Coherency","articles/dma-cache-coherency.html"]]},
    io:{title:"Hardware Interfaces",kicker:"WORLD 07 · BUS & PERIPHERALS",description:"Investigate the protocols and transactions that connect processors to devices.",articles:[["PCIe Bring-Up: A Debugging Checklist","articles/pcie-bringup-debugging.html"],["Platform, I²C, and SPI Drivers","articles/linux-platform-i2c-spi-drivers.html"],["NOR vs. NAND Flash","articles/nor-vs-nand.html"]]},
    debug:{title:"Interrupts & Debugging",kicker:"WORLD 08 · TIMING & RELIABILITY",description:"Diagnose events, latency, and failures using a systematic hardware-to-software approach.",articles:[["Interrupts vs. Polling vs. DMA","articles/interrupts-polling-dma.html"],["Process Context vs. Hard IRQ Context","articles/interrupt-context-vs-process-context.html"],["PCIe Bring-Up: A Debugging Checklist","articles/pcie-bringup-debugging.html"]]}
  };
  const hero=document.querySelector(".solar-hero");
  if(!hero)return;
  const panel=document.querySelector("#solarArticlePanel"), title=document.querySelector("#panelTitle"), kicker=document.querySelector("#panelKicker"), description=document.querySelector("#panelDescription"), list=document.querySelector("#panelArticles"), all=document.querySelector("#panelAll");
  const planets=[...document.querySelectorAll(".planet[data-world]")];
  let active=null;
  function close(){active=null;panel.hidden=true;hero.classList.remove("world-open");planets.forEach(p=>p.classList.remove("is-active")); }
  function open(key){const w=worlds[key];if(!w)return;active=key;title.textContent=w.title;kicker.textContent=w.kicker;description.textContent=w.description;list.replaceChildren();w.articles.forEach(([name,href])=>{const a=document.createElement("a");a.className="panel-article";a.href=href;a.textContent=name;list.appendChild(a)});all.href="#articles";all.textContent="Browse all articles ↗";panel.hidden=false;hero.classList.add("world-open");planets.forEach(p=>p.classList.toggle("is-active",p.dataset.world===key));}
  planets.forEach(p=>p.addEventListener("click",()=>active===p.dataset.world?close():open(p.dataset.world)));
  document.querySelector("#closeSolarPanel")?.addEventListener("click",close);
  document.addEventListener("keydown",e=>{if(e.key==="Escape"&&!panel.hidden)close()});
  document.querySelectorAll('.nav-links a[href="#topics"],.footer-links a[href="#topics"]').forEach(a=>a.setAttribute("href","#solar-system"));
  const search=document.querySelector("#solarSearch");
  search?.addEventListener("input",()=>{const q=search.value.trim().toLowerCase();if(!q){close();return}const found=Object.entries(worlds).find(([,w])=>w.title.toLowerCase().includes(q)||w.articles.some(([n])=>n.toLowerCase().includes(q)));if(found)open(found[0]);});


  // Move the topic worlds around the CPU along elliptical orbits continuously.
  const orbitSpecs={
    boot:{rx:.29,ry:.27,phase:3.8,speed:.19},
    arch:{rx:.12,ry:.15,phase:4.8,speed:.27},
    os:{rx:.31,ry:.29,phase:5.7,speed:.16},
    drivers:{rx:.40,ry:.08,phase:6.1,speed:.13},
    memory:{rx:.16,ry:.39,phase:1.6,speed:.21},
    multi:{rx:.32,ry:.30,phase:.7,speed:-.17},
    io:{rx:.41,ry:.13,phase:3.3,speed:.14},
    debug:{rx:.28,ry:.30,phase:2.6,speed:-.20}
  };
  const orbitStart=performance.now();
  let orbitFrame=0;
  function animatePlanets(now){
    const stage=document.querySelector("#solarStage");
    if(!stage)return;
    const rect=stage.getBoundingClientRect();
    const baseWidth=stage.offsetWidth,baseHeight=stage.offsetHeight;
    const mobileScale=window.innerWidth<=380?.49:window.innerWidth<=650?.57:window.innerWidth<=1100?.87:1;
    // Position in the unscaled stage coordinate system so it remains centered on the CPU.
    const cx=baseWidth/2,cy=baseHeight*.51;
    const elapsed=(now-orbitStart)/1000;
    planets.forEach(p=>{
      const spec=orbitSpecs[p.dataset.world];if(!spec)return;
      const angle=spec.phase+elapsed*spec.speed;
      const rx=Math.min(baseWidth*.44,baseWidth*spec.rx);
      const ry=Math.min(baseHeight*.43,baseHeight*spec.ry);
      const x=cx+Math.cos(angle)*rx;
      const y=cy+Math.sin(angle)*ry;
      p.style.left=(x-p.offsetWidth/2)+"px";
      p.style.top=(y-p.offsetHeight/2)+"px";
    });
    orbitFrame=requestAnimationFrame(animatePlanets);
  }
  if(!window.matchMedia("(prefers-reduced-motion: reduce)").matches)orbitFrame=requestAnimationFrame(animatePlanets);

  // Scroll progress gently zooms the solar system in, then out as the visitor moves past it.
  let scrollFrame=0;
  function updateScrollZoom(){
    scrollFrame=0;
    const rect=hero.getBoundingClientRect();
    const vh=window.innerHeight||800;
    const progress=Math.max(0,Math.min(1,(vh-rect.top)/(vh+rect.height)));
    const zoom=1+0.2*Math.sin(progress*Math.PI);
    hero.style.setProperty("--scroll-zoom",zoom.toFixed(3));
    const stage=document.querySelector("#solarStage");
    if(stage)stage.style.setProperty("--scroll-zoom",zoom.toFixed(3));
  }
  function requestScrollZoom(){if(!scrollFrame)scrollFrame=requestAnimationFrame(updateScrollZoom);}
  window.addEventListener("scroll",requestScrollZoom,{passive:true});
  window.addEventListener("resize",requestScrollZoom);
  updateScrollZoom();

})();