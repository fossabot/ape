from peewee import *
import os

database = SqliteDatabase(os.path.expanduser('~/'+'vFeed/vfeed.db'), **{})


class BaseModel(Model):
    class Meta:
        database = database

class NvdDb(BaseModel):
    cveid = TextField(null=True, primary_key=True)
    cvss_access_complexity = TextField(null=True)
    cvss_access_vector = TextField(null=True)
    cvss_authentication = TextField(null=True)
    cvss_availability_impact = TextField(null=True)
    cvss_base = TextField(null=True)
    cvss_confidentiality_impact = TextField(null=True)
    cvss_exploit = TextField(null=True)
    cvss_impact = TextField(null=True)
    cvss_integrity_impact = TextField(null=True)
    date_modified = DateField(null=True)
    date_published = DateField(null=True)
    summary = TextField(null=True)

    class Meta:
        db_table = 'nvd_db'

class CveCpe(BaseModel):
    cpeid = TextField(null=True)  # name
    cveid = ForeignKeyField(db_column='cveid', rel_model=NvdDb, to_field='cveid')

    class Meta:
        db_table = 'cve_cpe'

class CveCwe(BaseModel):
    cveid = ForeignKeyField(db_column='cveid', rel_model=NvdDb, to_field='cveid')
    cweid = TextField(null=True)  # name

    class Meta:
        db_table = 'cve_cwe'

class CveReference(BaseModel):
    cveid = ForeignKeyField(db_column='cveid', rel_model=NvdDb, to_field='cveid')
    refname = TextField(null=True)  # name
    refsource = TextField(null=True)  # name

    class Meta:
        db_table = 'cve_reference'

class CweDb(BaseModel):
    cweid = TextField(null=True)  # name
    cwetitle = TextField(null=True)  # name

    class Meta:
        db_table = 'cwe_db'

class CweCapec(BaseModel):
    capecid = TextField(null=True)  # name
    cweid = ForeignKeyField(db_column='cweid', rel_model=CweDb, to_field='cweid')

    class Meta:
        db_table = 'cwe_capec'

class CweCategory(BaseModel):
    categoryid = TextField(null=True)  # name
    categorytitle = TextField(null=True)  # name
    cweid = TextField(null=True)

    class Meta:
        db_table = 'cwe_category'

class MapCveAixapar(BaseModel):
    aixaparid = TextField(null=True)  # name
    cveid = ForeignKeyField(db_column='cveid', rel_model=NvdDb, to_field='cveid')

    class Meta:
        db_table = 'map_cve_aixapar'

class MapCveBid(BaseModel):
    bidid = TextField(null=True)  # name
    cveid = ForeignKeyField(db_column='cveid', rel_model=NvdDb, to_field='cveid')

    class Meta:
        db_table = 'map_cve_bid'

class MapCveCertvn(BaseModel):
    certvuid = TextField(null=True)  # name
    certvulink = TextField(null=True)  # name
    cveid = ForeignKeyField(db_column='cveid', rel_model=NvdDb, to_field='cveid')

    class Meta:
        db_table = 'map_cve_certvn'

class MapCveCisco(BaseModel):
    ciscoid = TextField(null=True)  # name
    cveid = ForeignKeyField(db_column='cveid', rel_model=NvdDb, to_field='cveid')

    class Meta:
        db_table = 'map_cve_cisco'

class MapCveD2(BaseModel):
    cveid = ForeignKeyField(db_column='cveid', rel_model=NvdDb, to_field='cveid')
    d2_script_file = TextField(null=True)  # name
    d2_script_name = TextField(null=True)  # name

    class Meta:
        db_table = 'map_cve_d2'

class MapCveDebian(BaseModel):
    cveid = ForeignKeyField(db_column='cveid', rel_model=NvdDb, to_field='cveid')
    debianid = TextField(null=True)  # name

    class Meta:
        db_table = 'map_cve_debian'

class MapCveExploitdb(BaseModel):
    cveid = ForeignKeyField(db_column='cveid', rel_model=NvdDb, to_field='cveid')
    exploitdbid = TextField(null=True)  # name
    exploitdbscript = TextField(null=True)  # name

    class Meta:
        db_table = 'map_cve_exploitdb'

class MapCveFedora(BaseModel):
    cveid = ForeignKeyField(db_column='cveid', rel_model=NvdDb, to_field='cveid')
    fedoraid = TextField(null=True)  # name

    class Meta:
        db_table = 'map_cve_fedora'

class MapCveGentoo(BaseModel):
    cveid = ForeignKeyField(db_column='cveid', rel_model=NvdDb, to_field='cveid')
    gentooid = TextField(null=True)  # name

    class Meta:
        db_table = 'map_cve_gentoo'

class MapCveHp(BaseModel):
    cveid = ForeignKeyField(db_column='cveid', rel_model=NvdDb, to_field='cveid')
    hpid = TextField(null=True)  # name
    hplink = TextField(null=True)  # name

    class Meta:
        db_table = 'map_cve_hp'

class MapCveIavm(BaseModel):
    cveid = ForeignKeyField(db_column='cveid', rel_model=NvdDb, to_field='cveid')
    disakey = TextField(null=True)  # name
    iavmid = TextField(null=True)  # name
    iavmtitle = TextField(null=True)  # name

    class Meta:
        db_table = 'map_cve_iavm'

class MapCveMandriva(BaseModel):
    cveid = ForeignKeyField(db_column='cveid', rel_model=NvdDb, to_field='cveid')
    mandrivaid = TextField(null=True)  # name

    class Meta:
        db_table = 'map_cve_mandriva'

class MapCveMilw0Rm(BaseModel):
    cveid = ForeignKeyField(db_column='cveid', rel_model=NvdDb, to_field='cveid')
    milw0rmid = TextField(null=True)  # name

    class Meta:
        db_table = 'map_cve_milw0rm'

class MapCveMs(BaseModel):
    cveid = ForeignKeyField(db_column='cveid', rel_model=NvdDb, to_field='cveid')
    msid = TextField(null=True)  # name
    mstitle = TextField(null=True)  # name

    class Meta:
        db_table = 'map_cve_ms'

class MapCveMsf(BaseModel):
    cveid = ForeignKeyField(db_column='cveid', rel_model=NvdDb, to_field='cveid')
    msf_script_file = TextField(null=True)  # name
    msf_script_name = TextField(null=True)  # name
    msfid = TextField(null=True)  # name

    class Meta:
        db_table = 'map_cve_msf'

class MapCveMskb(BaseModel):
    cveid = ForeignKeyField(db_column='cveid', rel_model=NvdDb, to_field='cveid')
    mskbid = TextField(null=True)  # name
    mskbtitle = TextField(null=True)  # name

    class Meta:
        db_table = 'map_cve_mskb'

class MapCveNessus(BaseModel):
    cveid = ForeignKeyField(db_column='cveid', rel_model=NvdDb, to_field='cveid')
    nessus_script_family = TextField(null=True)  # name
    nessus_script_file = TextField(null=True)  # name
    nessus_script = TextField(db_column='nessus_script_id', null=True)  # name
    nessus_script_name = TextField(null=True)  # name

    class Meta:
        db_table = 'map_cve_nessus'

class MapCveNmap(BaseModel):
    cveid = ForeignKeyField(db_column='cveid', rel_model=NvdDb, to_field='cveid')
    nmap_script_cat = TextField(null=True)  # name
    nmap_script = TextField(db_column='nmap_script_id', null=True)  # name

    class Meta:
        db_table = 'map_cve_nmap'

class MapCveOpenvas(BaseModel):
    cveid = ForeignKeyField(db_column='cveid', rel_model=NvdDb, to_field='cveid')
    openvas_script_family = TextField(null=True)  # name
    openvas_script_file = TextField(null=True)  # name
    openvas_script = TextField(db_column='openvas_script_id', null=True)  # name
    openvas_script_name = TextField(null=True)  # name

    class Meta:
        db_table = 'map_cve_openvas'

class MapCveOsvdb(BaseModel):
    cveid = ForeignKeyField(db_column='cveid', rel_model=NvdDb, to_field='cveid')
    osvdbid = TextField(null=True)  # name

    class Meta:
        db_table = 'map_cve_osvdb'

class MapCveOval(BaseModel):
    cpeid = TextField(null=True)  # name
    cveid = ForeignKeyField(db_column='cveid', rel_model=NvdDb, to_field='cveid')
    ovalclass = TextField(null=True)  # name
    ovalid = TextField(null=True)  # name
    ovaltitle = TextField(null=True)  # name

    class Meta:
        db_table = 'map_cve_oval'

class MapCveRedhat(BaseModel):
    cveid = ForeignKeyField(db_column='cveid', rel_model=NvdDb, to_field='cveid')
    redhatid = TextField(null=True)  # name
    redhatovalid = TextField(null=True)  # name
    redhatupdatedesc = TextField(null=True)  # name

    class Meta:
        db_table = 'map_cve_redhat'

class MapCveSaint(BaseModel):
    cveid = ForeignKeyField(db_column='cveid', rel_model=NvdDb, to_field='cveid')
    saintexploitid = TextField(null=True)  # name
    saintexploitlink = TextField(null=True)  # name
    saintexploittitle = TextField(null=True)  # name

    class Meta:
        db_table = 'map_cve_saint'

class MapCveScip(BaseModel):
    cveid = ForeignKeyField(db_column='cveid', rel_model=NvdDb, to_field='cveid')
    scipid = TextField(null=True)  # name
    sciplink = TextField(null=True)  # name

    class Meta:
        db_table = 'map_cve_scip'

class MapCveSnort(BaseModel):
    cveid = ForeignKeyField(db_column='cveid', rel_model=NvdDb, to_field='cveid')
    snort_classtype = TextField(null=True)  # name
    snort = TextField(db_column='snort_id', null=True)  # name
    snort_sig = TextField(null=True)  # name

    class Meta:
        db_table = 'map_cve_snort'

class MapCveSuricata(BaseModel):
    cveid = ForeignKeyField(db_column='cveid', rel_model=NvdDb, to_field='cveid')
    suricata_classtype = TextField(null=True)  # name
    suricata = TextField(db_column='suricata_id', null=True)  # name
    suricata_sig = TextField(null=True)  # name

    class Meta:
        db_table = 'map_cve_suricata'

class MapCveSuse(BaseModel):
    cveid = ForeignKeyField(db_column='cveid', rel_model=NvdDb, to_field='cveid')
    suseid = TextField(null=True)  # name

    class Meta:
        db_table = 'map_cve_suse'

class MapCveUbuntu(BaseModel):
    cveid = ForeignKeyField(db_column='cveid', rel_model=NvdDb, to_field='cveid')
    ubuntuid = TextField(null=True)  # name

    class Meta:
        db_table = 'map_cve_ubuntu'

class MapCveVmware(BaseModel):
    cveid = ForeignKeyField(db_column='cveid', rel_model=NvdDb, to_field='cveid')
    vmwareid = TextField(null=True)  # name

    class Meta:
        db_table = 'map_cve_vmware'

class MapRedhatBugzilla(BaseModel):
    advisory_dateissue = TextField(null=True)  # name
    bugzillaid = TextField(null=True)  # name
    bugzillatitle = TextField(null=True)  # name
    redhatid = ForeignKeyField(db_column='redhatid', rel_model=MapCveRedhat, to_field='redhatid')

    class Meta:
        db_table = 'map_redhat_bugzilla'

class StatNewCve(BaseModel):
    new_cve = TextField(db_column='new_cve_id', null=True)  # name
    new_cve_summary = TextField(null=True)  # name

    class Meta:
        db_table = 'stat_new_cve'

class StatVfeedKpi(BaseModel):
    db_version = TextField(null=True)  # name
    total_aixapar = TextField(null=True)  # name
    total_bid = TextField(null=True)  # name
    total_capec = TextField(null=True)  # name
    total_certvu = TextField(null=True)  # name
    total_cisco = TextField(null=True)  # name
    total_cpe = TextField(null=True)  # name
    total_cve = TextField(null=True)  # name
    total_cwe = TextField(null=True)  # name
    total_d2exploit = TextField(null=True)  # name
    total_debian = TextField(null=True)  # name
    total_exploitdb = TextField(null=True)  # name
    total_fedora = TextField(null=True)  # name
    total_gentoo = TextField(null=True)  # name
    total_hp = TextField(null=True)  # name
    total_iavm = TextField(null=True)  # name
    total_mandriva = TextField(null=True)  # name
    total_milw0rm = TextField(null=True)  # name
    total_ms = TextField(null=True)  # name
    total_msf = TextField(null=True)  # name
    total_mskb = TextField(null=True)  # name
    total_nessus = TextField(null=True)  # name
    total_nmap = TextField(null=True)  # name
    total_openvas = TextField(null=True)  # name
    total_osvdb = TextField(null=True)  # name
    total_oval = TextField(null=True)  # name
    total_redhat = TextField(null=True)  # name
    total_redhat_bugzilla = TextField(null=True)  # name
    total_saint = TextField(null=True)  # name
    total_scip = TextField(null=True)  # name
    total_snort = TextField(null=True)  # name
    total_suricata = TextField(null=True)  # name
    total_suse = TextField(null=True)  # name
    total_ubuntu = TextField(null=True)  # name
    total_vmware = TextField(null=True)  # name

    class Meta:
        db_table = 'stat_vfeed_kpi'
