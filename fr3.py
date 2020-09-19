w = 512
h = 512
# Pick initial positions for the nodes.
vs = [0]
es = []
pos = []

num_nodes = 128
for i in range(1, num_nodes):
    degs = []
    for v in vs:
        v_deg = len([e for e in es if e[0] == v or e[1] == v])
        degs.append(v_deg)
    
    for v in vs:
        prob = (degs[v] * 1.0 + 1) / (sum(degs) + 1)
        if random(0, 1) < prob:
            es.append([v, i])
    
    vs.append(i)

degs = []
for v in vs:
        v_deg = len([e for e in es if e[0] == v or e[1] == v])
        degs.append(v_deg)

for v in vs:
    pos.append([random(0, w), random(0, h)])
    
iters = 100
temp = 5
dt = 0.001

def setup():
    size(w, h)
    rect(0, 0, w, h)

# Fruchterman-Reingold algorithm.
# Every node is repelled by all other nodes
# inversely proportional to their squared distance.
# Every node is attracted to its graph neighbors
# proportional to their squared distance.
def fr(vs, es, pos, iters=100, t=0.1):
    k = sqrt(w*h * 1.0 / len(vs))
    
    for iter in range(iters):
        d_pos = [[0, 0] for _ in range(len(vs))]
        
        # Calculate all |vs|^2 repulsive forces
        for v in vs:
            for u in vs:
                dx = pos[v][0] - pos[u][0]
                dy = pos[v][1] - pos[u][1]
                delta = sqrt(dx**2 + dy**2)
                if delta != 0:
                    f_repulse = k**2 * 1.0 / delta
                    d_pos[v][0] += dx * f_repulse
                    d_pos[v][1] += dy * f_repulse
        
        # Calculate all |es| attractive forces
        for e in es:
            (v, u) = e
            dx = pos[v][0] - pos[u][0]
            dy = pos[v][1] - pos[u][1]
            delta = sqrt(dx**2 + dy**2)
            if delta != 0:
                f_attract = delta**2 * 1.0 / k
                d_pos[v][0] -= dx * f_attract
                d_pos[v][1] -= dy * f_attract
                d_pos[u][0] += dx * f_attract
                d_pos[u][1] += dy * f_attract
        
        # Cap movement by a cooling temperature parameter
        for v in vs:
            dx = d_pos[v][0]
            dy = d_pos[v][1]
            delta = sqrt(dx**2 + dy**2)
            if delta != 0:
                scale_fac = min(delta, t) * 1.0 / delta
                dx *= scale_fac
                dy *= scale_fac
                d_pos[v] = [dx, dy]
            
        # Return the new positions
        new_pos = []
        for i in range(len(pos)):
            new_pos.append([pos[i][0]+d_pos[i][0], pos[i][1]+d_pos[i][1]])
        return new_pos

min_temp = 0

go = True
def draw():
    global go
    if go:
        global pos
        global temp
        global iters
        pos = fr(vs, es, pos, t=temp)
        min_x = min(pos, key=lambda x: x[0])[0]
        min_y = min(pos, key=lambda y: y[1])[1]
        max_x = max(pos, key=lambda x: x[0])[0]
        max_y = max(pos, key=lambda y: y[1])[1]
        
        x_span = (max_x - min_x)
        y_span = (max_y - min_y)
        
        new_pos = []
        for p in pos:
            new_x = (p[0] - min_x) * w * 1.0 / x_span
            new_y = (p[1] - min_y) * h * 1.0 / y_span
            new_pos.append([new_x, new_y])
        pos = new_pos
        
        fill(255, 1)
        #rect(0, 0, w, h)
        # draw lines
        clr = 0
        if temp < 0:
            clr = 0
        for i in range(len(pos)):
            fill(135, 206, 235, 256*degs[i]*1.0/sum(degs))
            stroke(0, 0, 0, 0)
            circle(pos[i][0], pos[i][1], degs[i]+1)
            for j in range(len(pos)):
                if [i, j] in es:
                    dx = pos[i][0]-pos[j][0]
                    dy = pos[i][1]-pos[j][1]
                    dst = sqrt(dx**2 + dy**2) * 1.0 / sqrt(w*h)
                    alph = 8
                    stroke(clr,alph*dst)
                    line(pos[i][0], pos[i][1], pos[j][0], pos[j][1])
        temp = max(min_temp, temp-dt)
        if temp >= -dt and temp <= dt:
            print('flip')
        if temp == min_temp:
            go = False
            print('stop')
