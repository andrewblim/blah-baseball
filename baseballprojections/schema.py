from sqlalchemy import Column, Boolean, Integer, Float, String, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy.schema import UniqueConstraint
import datetime

Base = declarative_base()

class Player(Base):

    __tablename__ = 'players'

    id  = Column(Integer, primary_key=True)
    type = Column(String(20))

    mlb_id        = Column(String(20))
    retrosheet_id = Column(String(20))
    bp_id         = Column(String(20))
    fg_id         = Column(String(20))
    lahman_id     = Column(String(20))
    steamer_id    = Column(String(20))

    last_name  = Column(String(50))
    first_name = Column(String(50))
    birthdate  = Column(Date)

    __mapper_args__ = {
        'polymorphic_identity': 'players',
        'polymorphic_on': type
    }

    def age(self, from_date=datetime.date.today()):
        return (from_date - self.birthdate)

    def prettyprint(self):
        print('%s, %s (id: %d, FG ID: %s)' % \
              (self.last_name, self.first_name, self.id, self.fg_id))

    @classmethod
    def id_fields(cls):
        return ['mlb_id', 'retrosheet_id', 'bp_id', 'fg_id', 
                'lahman_id', 'steamer_id']

    @classmethod
    def name_fields(cls):
        return ['last_name', 'first_name']

class Batter(Player):

#    __tablename__ = 'batters'
#    id = Column(Integer, ForeignKey('players.id'), primary_key=True)
    projections = relationship('BatterProjection', backref='batter')

    __mapper_args__ = {
        'polymorphic_identity': 'batters'
    }

    def __repr__(self):
        return '<Batter %d (%s, %s)>' % (self.id, self.last_name, self.first_name)

    def prettyprint(self):
        super(Batter, self).prettyprint()
        print()
        print('%26s : %5s %5s %3s %3s %3s %3s' % \
              ('Projection', 'OBP', 'SLG', 'HR', 'R', 'RBI', 'SB'))
        projections = sorted(self.projections, key=lambda x: (x.projection_system.name, x.projection_system.year))
        for proj in projections:
            statline = '%20s, %4d :' % \
                       (proj.projection_system.name, proj.projection_system.year)
            statline += (' %5.3f' % proj.obp) if proj.obp is not None else ' -----'
            statline += (' %5.3f' % proj.slg) if proj.slg is not None else ' -----'
            statline += (' %3d' % proj.hr) if proj.hr is not None else ' ---'
            statline += (' %3d' % proj.r) if proj.r is not None else ' ---'
            statline += (' %3d' % proj.rbi) if proj.rbi is not None else ' ---'
            statline += (' %3d' % proj.sb) if proj.sb is not None else ' ---'
            print(statline)

class Pitcher(Player):

#    __tablename__ = 'pitchers'
#    id = Column(Integer, ForeignKey('players.id'), primary_key=True)
    projections = relationship('PitcherProjection', backref='pitcher')

    __mapper_args__ = {
        'polymorphic_identity': 'pitchers'
    }

    def __repr__(self):
        return '<Pitcher %d (%s, %s)>' % (self.id, self.last_name, self.first_name)

    def prettyprint(self):
        super(Pitcher, self).prettyprint()
        print()
        print('%26s : %3s %3s %5s %3s %5s %5s' % \
              ('Projection', 'W', 'SV', 'ERA', 'K', 'WHIP', 'IP'))
        projections = sorted(self.projections, key=lambda x: (x.projection_system.name, x.projection_system.year))
        for proj in projections:
            statline = '%20s, %4d :' % \
                       (proj.projection_system.name, proj.projection_system.year)
            statline += (' %3d' % proj.w) if proj.w is not None else ' ---'
            statline += (' %3d' % proj.sv) if proj.sv is not None else ' ---'
            statline += (' %5.2f' % proj.era) if proj.era is not None else ' -----'
            statline += (' %3d' % proj.k) if proj.k is not None else ' ---'
            statline += (' %5.3f' % proj.whip) if proj.whip is not None else ' -----'
            statline += (' %5.1f' % proj.ip) if proj.ip is not None else ' -----'
            print(statline)

class ProjectionSystem(Base):

    __tablename__ = 'projection_systems'
    id = Column(Integer, primary_key=True)

    name = Column(String(20))
    year = Column(Integer)
    is_actual = Column(Boolean)

    batter_projections = relationship('BatterProjection', backref='projection_system')
    pitcher_projections = relationship('PitcherProjection', backref='projection_system')

    __table_args__ = ( UniqueConstraint('name', 'year'), )

    def __repr__(self):
        return '<ProjectionSystem %d (%s, %d)>' % (self.id, self.name, self.year)

class BatterProjection(Base):

    __tablename__ = 'batter_projections'
    id = Column(Integer, primary_key=True)
    #batter_id = Column(Integer, ForeignKey('batters.id'))
    batter_id = Column(Integer, ForeignKey('players.id'))
    projection_system_id = Column(Integer, ForeignKey('projection_systems.id'))
    #UniqueConstraint('batter_id', 'projection_id')
    UniqueConstraint('batter_id', 'projection_system_id')

    team = Column(String(3))

    age  = Column(Float)
    g    = Column(Float)
    ab   = Column(Float)
    pa   = Column(Float)
    h    = Column(Float)
    h1b  = Column(Float)
    h2b  = Column(Float)
    h3b  = Column(Float)
    hr   = Column(Float)
    r    = Column(Float)
    rbi  = Column(Float)
    bb   = Column(Float)
    ibb  = Column(Float)
    k    = Column(Float)
    hbp  = Column(Float)
    sf   = Column(Float)
    sh   = Column(Float)
    gdp  = Column(Float)
    sb   = Column(Float)
    cs   = Column(Float)
    avg  = Column(Float)

    gb   = Column(Float)
    fb   = Column(Float)
    ld   = Column(Float)
    iffb = Column(Float)

    pitches = Column(Float)
    balls   = Column(Float)
    strikes = Column(Float)

    ifh = Column(Float)
    bu  = Column(Float)
    buh = Column(Float)

    bb_pct = Column(Float)
    k_pct  = Column(Float)
    bb_k   = Column(Float)

    obp   = Column(Float)
    slg   = Column(Float)
    ops   = Column(Float)
    iso   = Column(Float)
    babip = Column(Float)
    
    gb_fb    = Column(Float)
    ld_pct   = Column(Float)
    gb_pct   = Column(Float)
    fb_pct   = Column(Float)
    hr_fb    = Column(Float)
    iffb_pct = Column(Float)
    ifh_pct  = Column(Float)
    buh_pct  = Column(Float)

    woba = Column(Float)
    wraa = Column(Float)
    wrc  = Column(Float)

    bat = Column(Float)
    fld = Column(Float)
    rep = Column(Float)
    pos = Column(Float)

    rar     = Column(Float)
    war     = Column(Float)
    dollars = Column(Float)

    spd        = Column(Float)
    wrc_plus   = Column(Float)
    wpa        = Column(Float)
    wpa_minus  = Column(Float)
    wpa_plus   = Column(Float)
    re24       = Column(Float)
    rew        = Column(Float)
    pli        = Column(Float)
    phli       = Column(Float)
    ph         = Column(Float)
    wpali      = Column(Float)
    clutch     = Column(Float)

    fb_pct = Column(Float)
    fbv    = Column(Float)
    sl_pct = Column(Float)
    slv    = Column(Float)
    ct_pct = Column(Float)
    ctv    = Column(Float)
    cb_pct = Column(Float)
    cbv    = Column(Float)
    ch_pct = Column(Float)
    chv    = Column(Float)
    sf_pct = Column(Float)
    sfv    = Column(Float)
    kn_pct = Column(Float)
    knv    = Column(Float)

    xx_pct = Column(Float)
    po_pct = Column(Float)

    wfb  = Column(Float)
    wsl  = Column(Float)
    wct  = Column(Float)
    wcb  = Column(Float)
    wch  = Column(Float)
    wsf  = Column(Float)
    wkn  = Column(Float)
    wfbc = Column(Float)
    wslc = Column(Float)
    wctc = Column(Float)
    wcbc = Column(Float)
    wchc = Column(Float)
    wsfc = Column(Float)
    wknc = Column(Float)

    oswing_pct   = Column(Float)
    zswing_pct   = Column(Float)
    swing_pct    = Column(Float)
    ocontact_pct = Column(Float)
    zcontact_pct = Column(Float)
    contact_pct  = Column(Float)
    zone_pct     = Column(Float)
    fstrike_pct  = Column(Float)
    swstr_pct    = Column(Float)

    bsr = Column(Float)

    fa_pct_pfx = Column(Float)
    ft_pct_pfx = Column(Float)
    fc_pct_pfx = Column(Float)
    fs_pct_pfx = Column(Float)
    fo_pct_pfx = Column(Float)
    si_pct_pfx = Column(Float)
    sl_pct_pfx = Column(Float)
    cu_pct_pfx = Column(Float)
    kc_pct_pfx = Column(Float)
    ep_pct_pfx = Column(Float)
    ch_pct_pfx = Column(Float)
    sc_pct_pfx = Column(Float)
    kn_pct_pfx = Column(Float)
    un_pct_pfx = Column(Float)

    vfa_pfx = Column(Float)
    vft_pfx = Column(Float)
    vfc_pfx = Column(Float)
    vfs_pfx = Column(Float)
    vfo_pfx = Column(Float)
    vsi_pfx = Column(Float)
    vsl_pfx = Column(Float)
    vcu_pfx = Column(Float)
    vkc_pfx = Column(Float)
    vep_pfx = Column(Float)
    vch_pfx = Column(Float)
    vsc_pfx = Column(Float)
    vkn_pfx = Column(Float)

    fa_x_pfx = Column(Float)
    ft_x_pfx = Column(Float)
    fc_x_pfx = Column(Float)
    fs_x_pfx = Column(Float)
    fo_x_pfx = Column(Float)
    si_x_pfx = Column(Float)
    sl_x_pfx = Column(Float)
    cu_x_pfx = Column(Float)
    kc_x_pfx = Column(Float)
    ep_x_pfx = Column(Float)
    ch_x_pfx = Column(Float)
    sc_x_pfx = Column(Float)
    kn_x_pfx = Column(Float)

    fa_z_pfx = Column(Float)
    ft_z_pfx = Column(Float)
    fc_z_pfx = Column(Float)
    fs_z_pfx = Column(Float)
    fo_z_pfx = Column(Float)
    si_z_pfx = Column(Float)
    sl_z_pfx = Column(Float)
    cu_z_pfx = Column(Float)
    kc_z_pfx = Column(Float)
    ep_z_pfx = Column(Float)
    ch_z_pfx = Column(Float)
    sc_z_pfx = Column(Float)
    kn_z_pfx = Column(Float)

    wfa_pfx = Column(Float)
    wft_pfx = Column(Float)
    wfc_pfx = Column(Float)
    wfs_pfx = Column(Float)
    wfo_pfx = Column(Float)
    wsi_pfx = Column(Float)
    wsl_pfx = Column(Float)
    wcu_pfx = Column(Float)
    wkc_pfx = Column(Float)
    wep_pfx = Column(Float)
    wch_pfx = Column(Float)
    wsc_pfx = Column(Float)
    wkn_pfx = Column(Float)

    wfa_c_pfx = Column(Float)
    wft_c_pfx = Column(Float)
    wfc_c_pfx = Column(Float)
    wfs_c_pfx = Column(Float)
    wfo_c_pfx = Column(Float)
    wsi_c_pfx = Column(Float)
    wsl_c_pfx = Column(Float)
    wcu_c_pfx = Column(Float)
    wkc_c_pfx = Column(Float)
    wep_c_pfx = Column(Float)
    wch_c_pfx = Column(Float)
    wsc_c_pfx = Column(Float)
    wkn_c_pfx = Column(Float)

    oswing_pct_pfx   = Column(Float)
    zswing_pct_pfx   = Column(Float)
    swing_pct_pfx    = Column(Float)
    ocontact_pct_pfx = Column(Float)
    zcontact_pct_pfx = Column(Float)
    contact_pct_pfx  = Column(Float)
    zone_pct_pfx     = Column(Float)

    pace    = Column(Float)
    defense = Column(Float)
    wsb     = Column(Float)
    ubr     = Column(Float)
    off     = Column(Float)
    lg      = Column(Float)

    # positions = Column(String(20))
    # rookie = Column(Integer)

    positions = Column(String(20))
    rookie = Column(Integer)
    dc_fl = Column(String(2))

    def __repr__(self):
        return '<BatterProjection %d>' % (self.id)

class PitcherProjection(Base):

    __tablename__ = 'pitcher_projections'
    id = Column(Integer, primary_key=True)
    #pitcher_id = Column(Integer, ForeignKey('pitchers.id'))
    pitcher_id = Column(Integer, ForeignKey('players.id'))
    projection_system_id = Column(Integer, ForeignKey('projection_systems.id'))
    #UniqueConstraint('pitcher_id', 'projection_id')
    UniqueConstraint('pitcher_id', 'projection_system_id')

    team = Column(String(3))

    age = Column(Float)
    w   = Column(Float)
    l   = Column(Float)
    era = Column(Float)
    g   = Column(Float)
    gs  = Column(Float)
    cg  = Column(Float)
    sho = Column(Float)
    sv  = Column(Float)
    bs  = Column(Float)
    ip  = Column(Float)
    tbf = Column(Float)
    h   = Column(Float)
    r   = Column(Float)
    er  = Column(Float)
    hr  = Column(Float)
    bb  = Column(Float)
    ibb = Column(Float)
    hbp = Column(Float)
    wp  = Column(Float)
    bk  = Column(Float)
    k   = Column(Float)

    gb   = Column(Float)
    fb   = Column(Float)
    ld   = Column(Float)
    iffb = Column(Float)

    balls   = Column(Float)
    strikes = Column(Float)
    pitches = Column(Float)

    rs  = Column(Float)
    ifh = Column(Float)
    bu  = Column(Float)
    buh = Column(Float)

    k9      = Column(Float)
    bb9     = Column(Float)
    k_bb    = Column(Float)
    h9      = Column(Float)
    hr9     = Column(Float)
    avg     = Column(Float)
    whip    = Column(Float)
    babip   = Column(Float)
    lob_pct = Column(Float)
    fip     = Column(Float)
    
    gb_fb    = Column(Float)
    ld_pct   = Column(Float)
    gb_pct   = Column(Float)
    fb_pct   = Column(Float)
    iffb_pct = Column(Float)
    hr_fb    = Column(Float)
    ifh_pct  = Column(Float)
    buh_pct  = Column(Float)

    starting = Column(Float)
    start_ip = Column(Float)
    relieving = Column(Float)
    relief_ip = Column(Float)

    rar     = Column(Float)
    war     = Column(Float)
    dollars = Column(Float)

    tera = Column(Float)
    xfip = Column(Float)

    wpa        = Column(Float)
    wpa_minus  = Column(Float)
    wpa_plus   = Column(Float)
    re24       = Column(Float)
    rew        = Column(Float)
    pli        = Column(Float)
    inli       = Column(Float)
    gmli       = Column(Float)
    exli       = Column(Float)
    pulls      = Column(Float)
    wpali      = Column(Float)
    clutch     = Column(Float)

    fb_pct = Column(Float)
    fbv    = Column(Float)
    sl_pct = Column(Float)
    slv    = Column(Float)
    ct_pct = Column(Float)
    ctv    = Column(Float)
    cb_pct = Column(Float)
    cbv    = Column(Float)
    ch_pct = Column(Float)
    chv    = Column(Float)
    sf_pct = Column(Float)
    sfv    = Column(Float)
    kn_pct = Column(Float)
    knv    = Column(Float)

    xx_pct = Column(Float)
    po_pct = Column(Float)

    wfb  = Column(Float)
    wsl  = Column(Float)
    wct  = Column(Float)
    wcb  = Column(Float)
    wch  = Column(Float)
    wsf  = Column(Float)
    wkn  = Column(Float)
    wfbc = Column(Float)
    wslc = Column(Float)
    wctc = Column(Float)
    wcbc = Column(Float)
    wchc = Column(Float)
    wsfc = Column(Float)
    wknc = Column(Float)

    oswing_pct   = Column(Float)
    zswing_pct   = Column(Float)
    swing_pct    = Column(Float)
    ocontact_pct = Column(Float)
    zcontact_pct = Column(Float)
    contact_pct  = Column(Float)
    zone_pct     = Column(Float)
    fstrike_pct  = Column(Float)
    swstr_pct    = Column(Float)

    hld = Column(Float)
    sd  = Column(Float)
    md  = Column(Float)

    era_minus  = Column(Float)
    fip_minus  = Column(Float)
    xfip_minus = Column(Float)

    k_pct  = Column(Float)
    bb_pct = Column(Float)
    siera  = Column(Float)
    rs9    = Column(Float)
    ef     = Column(Float)

    fa_pct_pfx = Column(Float)
    ft_pct_pfx = Column(Float)
    fc_pct_pfx = Column(Float)
    fs_pct_pfx = Column(Float)
    fo_pct_pfx = Column(Float)
    si_pct_pfx = Column(Float)
    sl_pct_pfx = Column(Float)
    cu_pct_pfx = Column(Float)
    kc_pct_pfx = Column(Float)
    ep_pct_pfx = Column(Float)
    ch_pct_pfx = Column(Float)
    sc_pct_pfx = Column(Float)
    kn_pct_pfx = Column(Float)
    un_pct_pfx = Column(Float)

    vfa_pfx = Column(Float)
    vft_pfx = Column(Float)
    vfc_pfx = Column(Float)
    vfs_pfx = Column(Float)
    vfo_pfx = Column(Float)
    vsi_pfx = Column(Float)
    vsl_pfx = Column(Float)
    vcu_pfx = Column(Float)
    vkc_pfx = Column(Float)
    vep_pfx = Column(Float)
    vch_pfx = Column(Float)
    vsc_pfx = Column(Float)
    vkn_pfx = Column(Float)

    fa_x_pfx = Column(Float)
    ft_x_pfx = Column(Float)
    fc_x_pfx = Column(Float)
    fs_x_pfx = Column(Float)
    fo_x_pfx = Column(Float)
    si_x_pfx = Column(Float)
    sl_x_pfx = Column(Float)
    cu_x_pfx = Column(Float)
    kc_x_pfx = Column(Float)
    ep_x_pfx = Column(Float)
    ch_x_pfx = Column(Float)
    sc_x_pfx = Column(Float)
    kn_x_pfx = Column(Float)

    fa_z_pfx = Column(Float)
    ft_z_pfx = Column(Float)
    fc_z_pfx = Column(Float)
    fs_z_pfx = Column(Float)
    fo_z_pfx = Column(Float)
    si_z_pfx = Column(Float)
    sl_z_pfx = Column(Float)
    cu_z_pfx = Column(Float)
    kc_z_pfx = Column(Float)
    ep_z_pfx = Column(Float)
    ch_z_pfx = Column(Float)
    sc_z_pfx = Column(Float)
    kn_z_pfx = Column(Float)

    wfa_pfx = Column(Float)
    wft_pfx = Column(Float)
    wfc_pfx = Column(Float)
    wfs_pfx = Column(Float)
    wfo_pfx = Column(Float)
    wsi_pfx = Column(Float)
    wsl_pfx = Column(Float)
    wcu_pfx = Column(Float)
    wkc_pfx = Column(Float)
    wep_pfx = Column(Float)
    wch_pfx = Column(Float)
    wsc_pfx = Column(Float)
    wkn_pfx = Column(Float)

    wfa_c_pfx = Column(Float)
    wft_c_pfx = Column(Float)
    wfc_c_pfx = Column(Float)
    wfs_c_pfx = Column(Float)
    wfo_c_pfx = Column(Float)
    wsi_c_pfx = Column(Float)
    wsl_c_pfx = Column(Float)
    wcu_c_pfx = Column(Float)
    wkc_c_pfx = Column(Float)
    wep_c_pfx = Column(Float)
    wch_c_pfx = Column(Float)
    wsc_c_pfx = Column(Float)
    wkn_c_pfx = Column(Float)

    oswing_pct_pfx   = Column(Float)
    zswing_pct_pfx   = Column(Float)
    swing_pct_pfx    = Column(Float)
    ocontact_pct_pfx = Column(Float)
    zcontact_pct_pfx = Column(Float)
    contact_pct_pfx  = Column(Float)
    zone_pct_pfx     = Column(Float)

    pace    = Column(Float)
    ra9_war = Column(Float)

    bip_wins = Column(Float)
    lob_wins = Column(Float)
    fdp_wins = Column(Float)

    def __repr__(self):
        return '<PitcherProjection %d>' % (self.id)
