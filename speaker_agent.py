def find_speakers(speakers, expertise):
    q=(expertise or "").lower().strip(); out=[]
    for s in speakers:
        text=(s.expertise or "").lower(); score=100 if q and q in text else sum(10 for w in q.split() if w in text)
        out.append({"speaker":s.name,"expertise":s.expertise,"rating":s.rating,"match_score":score})
    return sorted(out,key=lambda x:x["match_score"],reverse=True)
