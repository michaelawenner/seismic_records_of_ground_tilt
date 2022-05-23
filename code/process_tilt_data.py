import obspy

def moving_average(x, w):
    return np.convolve(x, np.ones(w), 'valid') / w

def process_tilt_data(tm, t1, t2):
    """
    Process data from tiltmeters
    :param st: Stream containing horizontal and vertical compontents
    :type st: obspy.core.stream.Stream
    :param t1: time window before event
    :type t1: int
    :param t2: time after event
    :type t2: int
    """
    for tr in tm:
        tr.data = tr.data*0.03
    tm.detrend('demean')
    tm.detrend('linear')
    tm.taper(0.05)
    tm1 = tm.copy().filter('bandpass', freqmin=1/120, freqmax=1/10, zerophase=True, corners=2)
    #tm1 = tm.copy().filter('lowpass', freq=1/10, zerophase=False, corners=2)
    tm2 = tm1.copy()
    tmr = tm2.rotate('NE->RT', back_azimuth=55.+180.)
    tme = tmr.select(channel='BHR')
    #for tr, t in zip(tme, times[1:]):
    #    t = obspy.UTCDateTime(t)
    #    tr.trim(t - t1, t + t2)
    tme.detrend('linear') 
    return tme

def tilt_above_fc(st, inv):
    """
    Get tilt for frequencies above corner frequency (after Wielandt 1999)
    Assuming that all recorded ground velocity in this frequency is a result of tilt 
    rather than translational ground motion
    :param st: Stream containing horizontal and vertical compontents
    :type st: obspy.core.stream.Stream
    :param inv: Inventory containing belonging instrument responses
    :type inv: obspy.core.inventory.inventory.Inventory
    :return: obspy Stream containing rotatet seismic data converted to tilt in microradians
    """
    st1 = st.copy()
    inv = obspy.read_inventory(f'../data/USGS_seismic_data/response/usgs_{st[0].stats.station}_2016.xml')
    st1.filter('bandpass', freqmin=1/120, freqmax=1, corners=2, zerophase=False)
    st1.remove_response(inventory = inv, output = 'ACC', plot=False)
    st1.rotate(method='->ZNE', inventory=inv)
    st1.rotate('NE->RT', back_azimuth=55.+180.).detrend('demean')
    st1.detrend('demean')
    st1.taper(0.01)
    st1.filter('bandpass', freqmin=1/120, freqmax=1/10, corners = 2, zerophase=True)
    for tr in st1:
    #    tr.data -= 4.93e-11
        tr.data = tr.data/-9.81 *1e6
    return st1

def tilt_below_fc(st, inv, filt):
    """
    Get tilt for frequencies below corner frequency (after Aoyama 2008)
    :param st: Stream containing horizontal and vertical compontents
    :type st: obspy.core.stream.Stream
    :param inv: Inventory containing belonging instrument responses
    :type inv: obspy.core.inventory.inventory.Inventory
    :return: obspy Stream containing rotatet seismic data converted to tilt in microradians
    """
    st1 = st.copy()
    #st1.rotate(method='->ZNE', inventory=inv)
    #st1.rotate('NE->RT', back_azimuth=55.+180.).detrend('demean')
    fc = 1/120 # Corner frequency in Hz
    w0 = 2 * np.pi * fc
    sens = 1/st1[0].stats.response.instrument_sensitivity.value
    
    g = -9.81
    
    if filt =='bandpass':
        st1.filter('bandpass', freqmin = 1/(7200), freqmax=1/120, corners=2, zerophase=True)
    elif filt == 'lowpass':
        st1.filter('lowpass', freq = 1/120, corners=2, zerophase=True)
    st1.detrend('demean')
    st1.detrend('linear')
    st1.integrate()
    
    
    #st1.filter('lowpass', freq = 1/10, corners=2, zerophase=True)
    fac = (sens*(w0**2))/ g
    for tr in st1:
        tr.data = fac *tr.data *1e6
    return st1