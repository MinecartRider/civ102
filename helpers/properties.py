import numpy as np

def compute_section_properties(sections, point_of_interest=None):

    layers = []
    y_cursor = 0.0
    for item in sections:
        shape = 'rect'
        b = None
        h = None
        orient = 'up'

        if isinstance(item, dict):
            shape = item.get('shape', 'rect')
            b = float(item['b'])
            h = float(item['h'])
            orient = item.get('orientation', 'up')
        elif isinstance(item, (list, tuple)):
            if len(item) == 2:
                b = float(item[0]); h = float(item[1]); shape = 'rect'
            elif len(item) == 3 and isinstance(item[0], str):
                tag = item[0].lower()
                b = float(item[1]); h = float(item[2])
                if tag in ('tri', 'triangle', 'tri_up'):
                    shape = 'tri'; orient = 'up'
                elif tag in ('tri_down', 'triangle_down'):
                    shape = 'tri'; orient = 'down'
                else:
                    shape = 'rect'
            else:
                b = float(item[0]); h = float(item[1]); shape = 'rect'
        else:
            raise ValueError('Unsupported section spec: %r' % (item,))

        bottom = y_cursor
        top = y_cursor + h

        if shape == 'rect':
            A = b * h
            y_c = bottom + h / 2.0
            I_local = b * (h ** 3) / 12.0
        else:  # triangle
            A = 0.5 * b * h
            if orient == 'down':
                y_c = top - h / 3.0
            else:  # up
                y_c = bottom + h / 3.0
            I_local = b * (h ** 3) / 36.0

        layers.append({
            'shape': shape,
            'orientation': orient,
            'b': b,
            'h': h,
            'bottom': bottom,
            'top': top,
            'A': A,
            'y_c': y_c,
            'I_local': I_local,
        })
        y_cursor = top

    A_total = sum(L['A'] for L in layers)
    y_centroid = sum(L['A'] * L['y_c'] for L in layers) / A_total

    I_total = 0.0
    for L in layers:
        I_total += L['I_local'] + L['A'] * (L['y_c'] - y_centroid) ** 2

    if point_of_interest is None:
        ys = set()
        for L in layers:
            ys.add(L['bottom']); ys.add(L['top']); ys.add(L['y_c'])
        ys.add(y_centroid)
        y_queries = sorted(ys)
    else:
        if isinstance(point_of_interest, (list, tuple, set)):
            y_queries = [float(v) for v in point_of_interest]
        else:
            y_queries = [float(point_of_interest)]

    def Q_rect(b, bottom, top, yq):
        if top <= yq:
            return 0.0, 0.0
        overlap_bottom = max(bottom, yq)
        overlap_top = top
        h_part = overlap_top - overlap_bottom
        if h_part <= 0:
            return 0.0, 0.0
        A_part = b * h_part
        y_part = overlap_bottom + h_part / 2.0
        return A_part, y_part

    def Q_tri_up(b, bottom, top, h, yq):
        if yq <= bottom:
            A_part = 0.5 * b * h
            y_part = bottom + h / 3.0
            return A_part, y_part
        if yq >= top:
            return 0.0, 0.0
        h_above = top - yq
        A_part = 0.5 * b * (h_above ** 2) / h
        y_part = yq + h_above / 3.0
        return A_part, y_part

    def Q_tri_down(b, bottom, top, h, yq):
        A_full = 0.5 * b * h
        y_full = top - h / 3.0
        if yq <= bottom:
            return A_full, y_full
        if yq >= top:
            return 0.0, 0.0
        h_below = yq - bottom
        A_below = 0.5 * b * (h_below ** 2) / h
        y_below = bottom + h_below / 3.0  # centroid of the small 'up' triangle
        A_above = A_full - A_below
        y_above = (A_full * y_full - A_below * y_below) / A_above
        return A_above, y_above

    Q_map = {}
    for yq in y_queries:
        Q_sum = 0.0
        for L in layers:
            if L['shape'] == 'rect':
                A_part, y_part = Q_rect(L['b'], L['bottom'], L['top'], yq)
            else:
                if L['orientation'] == 'down':
                    A_part, y_part = Q_tri_down(L['b'], L['bottom'], L['top'], L['h'], yq)
                else:
                    A_part, y_part = Q_tri_up(L['b'], L['bottom'], L['top'], L['h'], yq)
            if A_part > 0.0:
                Q_sum += A_part * (y_part - y_centroid)
        Q_map[yq] = Q_sum

    section_meta = []
    for L in layers:
        section_meta.append({
            'shape': L['shape'],
            'orientation': L['orientation'] if L['shape'] == 'tri' else None,
            'b': L['b'],
            'h': L['h'],
            'bottom': L['bottom'],
            'top': L['top'],
            'centroid': L['y_c'],
            'A': L['A'],
        })

    return {
        'A_total': A_total,
        'y_centroid': y_centroid,
        'I': I_total,
        'Q': Q_map,
    }

def local_buckling(t, b, k, mu=0.2, E=4000):
    beta = np.pi**2 * E / (12 * (1 - mu**2))
    critical_stress = beta * k * (t/b)**2
    return critical_stress

def shear_buckling(t, b, a, k=5, mu=0.2, E=4000):
    beta = np.pi**2 * E / (12 * (1 - mu**2))
    critical_shear = beta * k * ((t/b)**2 + (t/a)**2)
    return critical_shear

def calculate_fos(sigma_applied, sigma_critical):
    return sigma_critical / sigma_applied
    

# print(compute_section_properties([(125, 300), (800, 100)], point_of_interest=286))
# print(local_buckling(2.54,50,0.425))
# print(shear_buckling(1.27, 200, 90))