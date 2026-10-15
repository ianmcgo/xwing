import pymupdf,json,re,sys,collections

ICON="X-WingIcons"

def items(pg):
    out=[]
    for b in pg.get_text("dict")["blocks"]:
        for l in b.get("lines",[]):
            for s in l["spans"]:
                t=s["text"]
                if not t.strip():
                    continue
                bb=s["bbox"]
                out.append({"x":bb[0],"y":bb[1],"x1":bb[2],"f":s["font"],"sz":s["size"],"t":t})
    return out

def join(parts):
    parts=sorted(parts,key=lambda p:(round(p["y"]/4),p["x"]))
    s=""
    for p in parts:
        if s and not s.endswith(" ") and not p["t"].startswith(" ") and p["f"]!=ICON and not s[-1] in "-/(":
            s+=" "
        s+=p["t"]
    return re.sub(r"\s+"," ",s).strip()

def parse_upgrades(path):
    d=pymupdf.open(path)
    recs=[]
    for pn,pg in enumerate(d):
        all_its=items(pg)
        hdr={}
        for i in all_its:
            if i["f"]=="KimberleyBl-Regular" and i["t"].strip() in ("Upgrade Name","Upgrade Type(s)","Cost","Restrictions","Standard","Extended"):
                hdr[i["t"].strip()]=i["x"]
        T=hdr.get("Upgrade Type(s)",192)-2
        C=hdr.get("Cost",279)-1
        R=hdr.get("Restrictions",311)-3
        Sx=hdr.get("Standard",458)-2
        Ex=hdr.get("Extended",514)-2
        its=[i for i in all_its if i["f"] not in ("KimberleyBl-Regular","MyriadPro-Regular","Avenir-Roman","EurostileLTStd-Cn") and i["y"]>190]
        anchors=[i for i in its if C<=i["x"]<R and re.fullmatch(r"-?\d+",i["t"].strip())]
        anchors.sort(key=lambda a:a["y"])
        ys=[a["y"] for a in anchors]
        rows=[{"y":a["y"],"parts":[]} for a in anchors]
        for i in its:
            if not ys:
                continue
            k=-1
            for n,y in enumerate(ys):
                if y<=i["y"]+3:
                    k=n
            if k>=0:
                rows[k]["parts"].append(i)
        for r in rows:
            cols=collections.defaultdict(list)
            for p in r["parts"]:
                x=p["x"]
                c="name" if x<T else "type" if x<C else "cost" if x<R else "res" if x<Sx else "std" if x<Ex else "ext"
                cols[c].append(p)
            recs.append({"page":pn+1,**{c:join(v).replace("\u00ad","") for c,v in cols.items()},"typeparts":sorted(cols["type"],key=lambda p:(round(p["y"]/4),p["x"]))})
    return recs

def parse_ships(path):
    d=pymupdf.open(path)
    recs=[]
    faction=None;ship=None
    for pn,pg in enumerate(d):
        its=[i for i in items(pg) if i["f"] not in ("MyriadPro-Regular","Avenir-Roman","EurostileLTStd-Cn")]
        hdr={}
        for i in its:
            if i["f"]=="KimberleyBl-Regular" and 150<i["y"]<190:
                hdr[i["t"].strip()]=i["x"]
        L=hdr.get("Loadout",hdr.get("Loadout Value",300))
        K=hdr.get("Keywords",456)
        Sx=hdr.get("Std.",520)
        Ex=hdr.get("Ext.",550)
        obl=[i["x"] for i in its if "Oblique" in i["f"] and i["x"]>100 and i["y"]>190]
        subx=(min(obl)-3) if obl else hdr.get("Subtitle",200)-30
        heads=[i for i in its if i["f"]=="KimberleyBl-Regular" and i["sz"]>20 and i["t"].strip()!="Ship Points Document"]
        shiphd=[i for i in its if i["f"].startswith("EurostileLTStd-Demi") and i["x"]<45]
        body=[i for i in its if i["f"]!="KimberleyBl-Regular" and i not in shiphd and i["y"]>150]
        anchors=[i for i in body if subx+80<=i["x"]<=L-5 and re.fullmatch(r"\d+",i["t"].strip())]
        anchors.sort(key=lambda a:a["y"])
        ys=[a["y"] for a in anchors]
        rows=[{"y":a["y"],"parts":[]} for a in anchors]
        for i in body:
            k=-1
            for n,y in enumerate(ys):
                if y<=i["y"]+3:
                    k=n
            if k>=0:
                rows[k]["parts"].append(i)
        events=[("f",h["y"],h["t"].strip()) for h in heads]+[("s",h["y"],h["t"].strip()) for h in shiphd]+[("r",r["y"],r) for r in rows]
        events.sort(key=lambda e:e[1])
        for kind,y,v in events:
            if kind=="f":
                faction=v
            elif kind=="s":
                ship=re.sub(r"\s*\(continued\)\s*$","",v)
            else:
                cols=collections.defaultdict(list)
                for q in v["parts"]:
                    x=q["x"]
                    c="name" if x<subx else "sub" if x<subx+80 and not re.fullmatch(r"\d+",q["t"].strip()) else "cost" if x<L-5 else "load" if x<L+35 else "bar" if x<K-8 else "kw" if x<Sx-10 else "std" if x<Ex-10 else "ext"
                    cols[c].append(q)
                recs.append({"page":pn+1,"faction":faction,"ship":ship,**{c:join(vv).replace("\u00ad","") for c,vv in cols.items()},"barparts":sorted(cols["bar"],key=lambda q:(round(q["y"]/4),q["x"]))})
    return recs

def finalize(raw,data2_dir):
    import glob
    def norm(s):
        return re.sub(r"[^a-z0-9]","",s.lower())
    sizes={}
    for f in glob.glob(data2_dir+"/data/pilots/*/*.json"):
        j=json.load(open(f))
        sizes[norm(j["name"])]=j["size"]
    FAC={"REBEL":"Rebel","IMPERIAL":"Imperial","SCUM AND VILLAINY":"Scum","REPUBLIC":"Republic","SEPARATIST":"Separatist","RESISTANCE":"Resistance","FIRST ORDER":"First Order"}
    TYPES=["Configuration","Force Power","Tactical Relay","Astromech","Modification","Illicit","Payload","Torpedo","Missile","Cannon","Sensor","Gunner","Talent","Title","Turret","Crew","Tech"]
    def legal(v):
        return "Banned" if "Ban" in v else "Yes" if "Yes" in v else "No" if "No" in v else ""
    pilots=[]
    shipnames=sorted(set(s["ship"] for s in raw["ships"]))
    for s in raw["ships"]:
        pilots.append([FAC[s["faction"]],s["ship"],s["name"],s["sub"],s["lim"],s["cost"],-1 if s["load"] is None else s["load"],[b for b in s["bar"] if not b.startswith("?")],s["kw"],legal(s["std"]),legal(s["ext"])])
    ups=[]
    for u in raw["upgrades"]:
        joined=" ".join(u["types"])
        found=[]
        for m in re.finditer("|".join(TYPES),joined):
            found.append(m.group(0))
        ups.append([u["name"],u["lim"],found,int(u["cost"]),re.sub(r"\s+-","-",re.sub(r"\s+"," ",u["res"])).strip(),legal(u["std"]),legal(u["ext"])])
    sz={}
    miss=[]
    for n in shipnames:
        k=norm(n)
        if k in sizes:
            sz[n]=sizes[k]
        else:
            cand=[v for kk,v in sizes.items() if kk.startswith(k) or k.startswith(kk)]
            if cand:
                sz[n]=cand[0]
            else:
                miss.append(n)
    return {"pilots":pilots,"upgrades":ups,"sizes":sz,"missing_sizes":miss}


if __name__=="__main__":
    ship_pdf,upg_pdf,out,data2=sys.argv[1:5]
    U=parse_upgrades(upg_pdf)
    gmap={}
    for r in U:
        txt="".join(p["t"] for p in r["typeparts"])
        m=re.match(r"^(.*?)\s*\((.*)\)\s*$",txt)
        if not m:
            continue
        names=[n.strip() for n in m.group(1).split(",")]
        icons=[c for c in m.group(2) if ord(c)>0xE000]
        if len(names)==len(icons):
            for n,c in zip(names,icons):
                gmap[c]=n
    upgrades=[]
    for r in U:
        txt="".join(p["t"] for p in r["typeparts"])
        clean="".join(c for c in txt if ord(c)<0xE000)
        clean=re.sub(r"[()\[\]]"," ",clean)
        types=[n.strip() for n in clean.split(",") if n.strip()]
        name=r["name"]
        bullets=len(name)-len(name.lstrip("•"))
        upgrades.append({"name":name.lstrip("•").strip(),"lim":bullets,"types":types,"cost":r.get("cost",""),"res":r.get("res",""),"std":r.get("std",""),"ext":r.get("ext","")})
    S=parse_ships(ship_pdf)
    ships=[]
    for r in S:
        name=r["name"]
        bullets=len(name)-len(name.lstrip("•"))
        bar=[gmap.get(c,"?"+hex(ord(c))) for c in "".join(p["t"] for p in r["barparts"]) if ord(c)>0xE000]
        ld=r.get("load","")
        ships.append({"faction":r["faction"],"ship":r["ship"],"name":name.lstrip("•").strip(),"lim":bullets,"sub":r.get("sub",""),"cost":int(r["cost"]),"load":None if ld in ("N/A","") else int(ld) if ld.isdigit() else ld,"bar":bar,"kw":r.get("kw",""),"std":r.get("std",""),"ext":r.get("ext","")})
    raw={"glyphs":{hex(ord(k)):v for k,v in gmap.items()},"ships":ships,"upgrades":upgrades}
    fin=finalize(raw,data2)
    json.dump(fin,open(out,"w"),ensure_ascii=False,separators=(",",":"))
    print(len(fin["pilots"]),"pilots",len(fin["upgrades"]),"upgrades",len(fin["sizes"]),"sizes","missing",fin["missing_sizes"])

