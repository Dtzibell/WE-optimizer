from PyQt6.QtWidgets import (
    QApplication,
    QCheckBox,
    QDoubleSpinBox,
    QFormLayout,
    QMainWindow,
    QSpinBox,
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
    QWidget,
)
from battle import DamageCalculator
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Damage maxer 3000")
        self.window_layout = QHBoxLayout()
        self.left_layout = QFormLayout()
        self.middle_layout = QFormLayout()
        self.right_layout = QFormLayout()
        self.damage_layout = QVBoxLayout()

        self.weaponBox = QSpinBox()
        self.weaponBox.setRange(0, 6)
        self.weaponBox.setValue(0)
        self.helmetBox = QSpinBox()
        self.helmetBox.setRange(0, 6)
        self.helmetBox.setValue(0)
        self.chestBox = QSpinBox()
        self.chestBox.setRange(0, 6)
        self.chestBox.setValue(0)
        self.glovesBox = QSpinBox()
        self.glovesBox.setRange(0, 6)
        self.glovesBox.setValue(0)
        self.pantsBox = QSpinBox()
        self.pantsBox.setRange(0, 6)
        self.pantsBox.setValue(0)
        self.bootsBox = QSpinBox()
        self.bootsBox.setRange(0, 6)
        self.bootsBox.setValue(0)
        self.bulletsBox = QSpinBox()
        self.bulletsBox.setRange(0, 3)
        self.bulletsBox.setValue(0)
        self.headquartersBox = QSpinBox()
        self.headquartersBox.setRange(0, 4)
        self.headquartersBox.setValue(0)
        self.skillPointsBox = QSpinBox()
        self.skillPointsBox.setRange(0, 120)
        self.skillPointsBox.setValue(0)
        self.countryBunkerBox = QSpinBox()
        self.countryBunkerBox.setRange(0, 5)
        self.countryBunkerBox.setValue(0)
        self.militaryBaseBox = QSpinBox()
        self.militaryBaseBox.setRange(0, 5)
        self.militaryBaseBox.setValue(0)
        self.countryOrderBox = QSpinBox()
        self.countryOrderBox.setRange(0, 3)
        self.countryOrderBox.setValue(0)
        self.muOrderBox = QSpinBox()
        self.muOrderBox.setRange(0, 3)
        self.muOrderBox.setValue(0)
        self.resistanceBox = QSpinBox()
        self.resistanceBox.setRange(0, 40)
        self.resistanceBox.setValue(0)

        self.coreRegionBox = QCheckBox()
        self.allyBox = QCheckBox()
        self.swornEnemyBox = QCheckBox()
        self.regionNotLinkedBox = QCheckBox()
        self.attackingRegionLostBox = QCheckBox()
        self.pillBox = QCheckBox()
        self.perHourBox = QCheckBox()

        self.knifePrice = QDoubleSpinBox()
        self.knifePrice.setRange(0, 1000)
        self.knifePrice.setValue(0)
        self.gunPrice = QDoubleSpinBox()
        self.gunPrice.setRange(0, 1000)
        self.gunPrice.setValue(0)
        self.riflePrice = QDoubleSpinBox()
        self.riflePrice.setRange(0, 1000)
        self.riflePrice.setValue(0)
        self.sniperPrice = QDoubleSpinBox()
        self.sniperPrice.setRange(0, 1000)
        self.sniperPrice.setValue(0)
        self.tankPrice = QDoubleSpinBox()
        self.tankPrice.setRange(0, 1000)
        self.tankPrice.setValue(0)
        self.jetPrice = QDoubleSpinBox()
        self.jetPrice.setRange(0, 1000)
        self.jetPrice.setValue(0)
        self.helmet1Price = QDoubleSpinBox()
        self.helmet1Price.setRange(0, 1000)
        self.helmet1Price.setValue(0)
        self.helmet2Price = QDoubleSpinBox()
        self.helmet2Price.setRange(0, 1000)
        self.helmet2Price.setValue(0)
        self.helmet3Price = QDoubleSpinBox()
        self.helmet3Price.setRange(0, 1000)
        self.helmet3Price.setValue(0)
        self.helmet4Price = QDoubleSpinBox()
        self.helmet4Price.setRange(0, 1000)
        self.helmet4Price.setValue(0)
        self.helmet5Price = QDoubleSpinBox()
        self.helmet5Price.setRange(0, 1000)
        self.helmet5Price.setValue(0)
        self.helmet6Price = QDoubleSpinBox()
        self.helmet6Price.setRange(0, 1000)
        self.helmet6Price.setValue(0)
        self.chest1Price = QDoubleSpinBox()
        self.chest1Price.setRange(0, 1000)
        self.chest1Price.setValue(0)
        self.chest2Price = QDoubleSpinBox()
        self.chest2Price.setRange(0, 1000)
        self.chest2Price.setValue(0)
        self.chest3Price = QDoubleSpinBox()
        self.chest3Price.setRange(0, 1000)
        self.chest3Price.setValue(0)
        self.chest4Price = QDoubleSpinBox()
        self.chest4Price.setRange(0, 1000)
        self.chest4Price.setValue(0)
        self.chest5Price = QDoubleSpinBox()
        self.chest5Price.setRange(0, 1000)
        self.chest5Price.setValue(0)
        self.chest6Price = QDoubleSpinBox()
        self.chest6Price.setRange(0, 1000)
        self.chest6Price.setValue(0)
        self.gloves1Price = QDoubleSpinBox()
        self.gloves1Price.setRange(0, 1000)
        self.gloves1Price.setValue(0)
        self.gloves2Price = QDoubleSpinBox()
        self.gloves2Price.setRange(0, 1000)
        self.gloves2Price.setValue(0)
        self.gloves3Price = QDoubleSpinBox()
        self.gloves3Price.setRange(0, 1000)
        self.gloves3Price.setValue(0)
        self.gloves4Price = QDoubleSpinBox()
        self.gloves4Price.setRange(0, 1000)
        self.gloves4Price.setValue(0)
        self.gloves5Price = QDoubleSpinBox()
        self.gloves5Price.setRange(0, 1000)
        self.gloves5Price.setValue(0)
        self.gloves6Price = QDoubleSpinBox()
        self.gloves6Price.setRange(0, 1000)
        self.gloves6Price.setValue(0)
        self.pants1Price = QDoubleSpinBox()
        self.pants1Price.setRange(0, 1000)
        self.pants1Price.setValue(0)
        self.pants2Price = QDoubleSpinBox()
        self.pants2Price.setRange(0, 1000)
        self.pants2Price.setValue(0)
        self.pants3Price = QDoubleSpinBox()
        self.pants3Price.setRange(0, 1000)
        self.pants3Price.setValue(0)
        self.pants4Price = QDoubleSpinBox()
        self.pants4Price.setRange(0, 1000)
        self.pants4Price.setValue(0)
        self.pants5Price = QDoubleSpinBox()
        self.pants5Price.setRange(0, 1000)
        self.pants5Price.setValue(0)
        self.pants6Price = QDoubleSpinBox()
        self.pants6Price.setRange(0, 1000)
        self.pants6Price.setValue(0)
        self.boots1Price = QDoubleSpinBox()
        self.boots1Price.setRange(0, 1000)
        self.boots1Price.setValue(0)
        self.boots2Price = QDoubleSpinBox()
        self.boots2Price.setRange(0, 1000)
        self.boots2Price.setValue(0)
        self.boots3Price = QDoubleSpinBox()
        self.boots3Price.setRange(0, 1000)
        self.boots3Price.setValue(0)
        self.boots4Price = QDoubleSpinBox()
        self.boots4Price.setRange(0, 1000)
        self.boots4Price.setValue(0)
        self.boots5Price = QDoubleSpinBox()
        self.boots5Price.setRange(0, 1000)
        self.boots5Price.setValue(0)
        self.boots6Price = QDoubleSpinBox()
        self.boots6Price.setRange(0, 1000)
        self.boots6Price.setValue(0)
        self.ammo1Price = QDoubleSpinBox()
        self.ammo1Price.setRange(0,2)
        self.ammo1Price.setValue(0)
        self.ammo2Price = QDoubleSpinBox()
        self.ammo2Price.setRange(0,2)
        self.ammo2Price.setValue(0)
        self.ammo3Price = QDoubleSpinBox()
        self.ammo3Price.setRange(0,2)
        self.ammo3Price.setValue(0)
        self.pillPrice = QDoubleSpinBox()
        self.pillPrice.setRange(0,40)
        self.pillPrice.setValue(0)
        
        available_sp = self.skillPointsBox.value()
        helmet = self.helmetBox.value()
        chest = self.chestBox.value()
        gloves = self.glovesBox.value()
        pants = self.pantsBox.value()
        boots = self.bootsBox.value()
        bullets = self.bulletsBox.value()
        weapon = self.weaponBox.value()
        country_bunker = self.countryBunkerBox.value() * 5
        military_base = self.militaryBaseBox.value() * 5
        country_order = self.countryOrderBox.value() * 5
        mu_order = self.muOrderBox.value() * 5
        headquarters = self.headquartersBox.value() * 5
        resistance = self.resistanceBox.value()
        pill = self.pillBox.isChecked()
        core_region = self.coreRegionBox.isChecked()
        ally = self.allyBox.isChecked()
        sworn_enemy = self.swornEnemyBox.isChecked()
        region_not_linked = self.regionNotLinkedBox.isChecked()
        attacking_region_lost = self.attackingRegionLostBox.isChecked()
        per_hour = self.perHourBox.isChecked()

        self.dcalc = DamageCalculator(
                 available_sp=available_sp,
                 helmetlvl=helmet,
                 chestlvl=chest,
                 gloveslvl=gloves,
                 pantslvl=pants,
                 bootslvl=boots,
                 ammolvl=bullets,
                 weaponlvl=weapon,
                 mu_hqlvl=headquarters,
                 country_bunkerlvl=country_bunker,
                 military_baselvl=military_base,
                 country_orderlvl=country_order,
                 mu_orderlvl=mu_order,
                 resistance=resistance,
                 is_pill=pill,
                 is_core_region=core_region,
                 is_ally=ally,
                 is_sworn_enemy=sworn_enemy,
                 is_region_not_linked=region_not_linked,
                 is_attacking_region_lost=attacking_region_lost,
                 is_per_hour=per_hour,
                 )
        dmg = self.dcalc.calc_upgrade()
        label = "\n".join(line.strip() for line in f"""Maximum damage: {dmg[0]:.2f}
                           Skills to achieve:
                           Attack: {dmg[1]["attack"]:.0f}
                           Precision: {dmg[1]["precision"]:.2f}
                           Critical chance: {dmg[1]["criticalChance"]:.2f}
                           Critical damage: {dmg[1]["criticalDamages"]:.2f}
                           Armor: {dmg[1]["armor"]:.2f}
                           Dodge: {dmg[1]["dodge"]:.2f}
                           Health: {dmg[1]["health"]:.0f}
                           """.splitlines())
        self.damage_label = QLabel("Damage report:")
        self.info = QLabel(label)
        self.damage_layout.addWidget(self.damage_label)
        self.damage_layout.addWidget(self.info)

        self.left_layout.addRow("Skill points", self.skillPointsBox)
        self.left_layout.addRow("Weapon level", self.weaponBox)
        self.left_layout.addRow("Bullets level", self.bulletsBox)
        self.left_layout.addRow("Helmet level", self.helmetBox)
        self.left_layout.addRow("Chest level", self.chestBox)
        self.left_layout.addRow("Gloves level", self.glovesBox)
        self.left_layout.addRow("Pants level", self.pantsBox)
        self.left_layout.addRow("Boots level", self.bootsBox)
        self.left_layout.addRow(
            "Military unit headquarter level", self.headquartersBox
        )
        self.left_layout.addRow("Military unit order level", self.muOrderBox)
        self.left_layout.addRow("Country order level", self.countryOrderBox)
        self.left_layout.addRow("Country bunker level", self.countryBunkerBox)
        self.left_layout.addRow("Military base level", self.militaryBaseBox)
        self.left_layout.addRow("Resistance level", self.resistanceBox)
        self.middle_layout.addRow("Pill?", self.pillBox)
        self.middle_layout.addRow("Ally?", self.allyBox)
        self.middle_layout.addRow("Sworn Enemy?", self.swornEnemyBox)
        self.middle_layout.addRow("Core region?", self.coreRegionBox)
        self.middle_layout.addRow(
            "Attacking region lost?", self.attackingRegionLostBox
        )
        self.middle_layout.addRow("Region not linked?", self.regionNotLinkedBox)
        self.middle_layout.addRow(
            "Damage over 8 hours?",
            self.perHourBox,
        )

        self.window_layout.addLayout(self.left_layout)
        self.window_layout.addLayout(self.middle_layout)
        self.window_layout.addLayout(self.damage_layout)
        self.widget = QWidget()
        self.widget.setLayout(self.window_layout)
        self.setCentralWidget(self.widget)

        self.skillPointsBox.valueChanged.connect(self.sp_changed)
        self.helmetBox.valueChanged.connect(self.helmet_changed)
        self.weaponBox.valueChanged.connect(self.weapon_changed)
        self.glovesBox.valueChanged.connect(self.gloves_changed)
        self.chestBox.valueChanged.connect(self.chest_changed)
        self.pantsBox.valueChanged.connect(self.pants_changed)
        self.bootsBox.valueChanged.connect(self.boots_changed)
        self.bulletsBox.valueChanged.connect(self.bullets_changed)
        self.perHourBox.checkStateChanged.connect(self.per_hour_changed)
        self.headquartersBox.valueChanged.connect(self.headquarters_changed)
        self.pillBox.checkStateChanged.connect(self.pill_changed)
        self.countryBunkerBox.valueChanged.connect(self.country_bunker_lvl_changed)
        self.countryOrderBox.valueChanged.connect(self.country_order_lvl_changed)
        self.militaryBaseBox.valueChanged.connect(self.military_base_lvl_changed)
        self.muOrderBox.valueChanged.connect(self.mu_order_lvl_changed)
        self.resistanceBox.valueChanged.connect(self.resistance_lvl_changed)
        self.allyBox.checkStateChanged.connect(self.ally_changed)
        self.swornEnemyBox.checkStateChanged.connect(self.sworn_enemy_changed)
        self.coreRegionBox.checkStateChanged.connect(self.core_region_changed)
        self.attackingRegionLostBox.checkStateChanged.connect(
            self.attacking_region_lost_changed
        )
        self.regionNotLinkedBox.checkStateChanged.connect(
            self.region_not_linked_changed
        )

    def helmet_changed(self):
        self.dcalc.set_helmet_lvl(self.helmetBox.value())
        self.info.setText(self.calc_upgrade())

    def chest_changed(self):
        self.dcalc.set_chest_lvl(self.chestBox.value())
        self.info.setText(self.calc_upgrade())

    def gloves_changed(self):
        self.dcalc.set_gloves_lvl(self.glovesBox.value())
        self.info.setText(self.calc_upgrade())

    def pants_changed(self):
        self.dcalc.set_pants_lvl(self.pantsBox.value())
        self.info.setText(self.calc_upgrade())

    def boots_changed(self):
        self.dcalc.set_boots_lvl(self.bootsBox.value())
        self.info.setText(self.calc_upgrade())

    def bullets_changed(self):
        self.dcalc.set_ammo_lvl(self.bulletsBox.value())
        self.info.setText(self.calc_upgrade())

    def weapon_changed(self):
        self.dcalc.set_weapon_lvl(self.weaponBox.value())
        self.info.setText(self.calc_upgrade())

    def headquarters_changed(self):
        self.dcalc.set_mu_hq_lvl(self.headquartersBox.value())
        self.info.setText(self.calc_upgrade())

    def mu_order_lvl_changed(self):
        self.dcalc.set_mu_order_lvl(self.muOrderBox.value())
        self.info.setText(self.calc_upgrade())

    def country_order_lvl_changed(self):
        self.dcalc.set_country_order_lvl(self.countryOrderBox.value())
        self.info.setText(self.calc_upgrade())

    def country_bunker_lvl_changed(self):
        self.dcalc.set_country_bunker_lvl(self.countryBunkerBox.value())
        self.info.setText(self.calc_upgrade())

    def military_base_lvl_changed(self):
        self.dcalc.set_military_base_lvl(self.militaryBaseBox.value())
        self.info.setText(self.calc_upgrade())

    def resistance_lvl_changed(self):
        self.dcalc.set_resistance(self.resistanceBox.value())
        self.info.setText(self.calc_upgrade())

    def per_hour_changed(self):
        self.dcalc.set_per_hour(self.perHourBox.isChecked())
        self.info.setText(self.calc_upgrade())

    def pill_changed(self):
        self.dcalc.set_pill(self.pillBox.isChecked())
        self.info.setText(self.calc_upgrade())

    def ally_changed(self):
        self.dcalc.set_ally(self.allyBox.isChecked())
        self.info.setText(self.calc_upgrade())

    def sworn_enemy_changed(self):
        self.dcalc.set_sworn_enemy(self.swornEnemyBox.isChecked())
        self.info.setText(self.calc_upgrade())

    def core_region_changed(self):
        self.dcalc.set_core_region(self.coreRegionBox.isChecked())
        self.info.setText(self.calc_upgrade())

    def attacking_region_lost_changed(self):
        self.dcalc.set_attacking_region_lost(self.attackingRegionLostBox.isChecked())
        self.info.setText(self.calc_upgrade())

    def region_not_linked_changed(self):
        self.dcalc.set_region_not_linked(self.regionNotLinkedBox.isChecked())
        self.info.setText(self.calc_upgrade())

    def sp_changed(self):
        self.dcalc.set_skill_points(self.skillPointsBox.value())
        self.info.setText(self.calc_upgrade())

    def calc_upgrade(self):
        dmg = self.dcalc.calc_upgrade()
        label = "\n".join(line.strip() for line in f"""Maximum damage: {dmg[0]:.2f}
                           Skills to achieve:
                           Attack: {dmg[1]["attack"]:.0f}
                           Precision: {dmg[1]["precision"]:.2f}
                           Critical chance: {dmg[1]["criticalChance"]:.2f}
                           Critical damage: {dmg[1]["criticalDamages"]:.2f}
                           Armor: {dmg[1]["armor"]:.2f}
                           Dodge: {dmg[1]["dodge"]:.2f}
                           Health: {dmg[1]["health"]:.0f}
                           """.splitlines())
        return label


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
