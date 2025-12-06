from PyQt6.QtWidgets import (
    QApplication,
    QCheckBox,
    QFormLayout,
    QMainWindow,
    QSpinBox,
    QVBoxLayout,
    QLabel,
    QWidget,
)
from battle import DamageCalculator
import sys
from textwrap import dedent

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Damage maxer 3000")
        self.window_layout = QVBoxLayout()
        self.parameter_layout = QFormLayout()

        self.weaponBox = QSpinBox()
        self.weaponBox.setRange(1, 6)
        self.weaponBox.setValue(1)
        self.helmetBox = QSpinBox()
        self.helmetBox.setRange(1, 6)
        self.helmetBox.setValue(1)
        self.chestBox = QSpinBox()
        self.chestBox.setRange(1, 6)
        self.chestBox.setValue(1)
        self.glovesBox = QSpinBox()
        self.glovesBox.setRange(1, 6)
        self.glovesBox.setValue(1)
        self.pantsBox = QSpinBox()
        self.pantsBox.setRange(1, 6)
        self.pantsBox.setValue(1)
        self.bootsBox = QSpinBox()
        self.bootsBox.setRange(1, 6)
        self.bootsBox.setValue(1)
        self.bulletsBox = QSpinBox()
        self.bulletsBox.setRange(1, 3)
        self.bulletsBox.setValue(0)
        self.headquartersBox = QSpinBox()
        self.headquartersBox.setRange(0, 4)
        self.headquartersBox.setValue(0)
        self.skillPointsBox = QSpinBox()
        self.skillPointsBox.setRange(0, 120)
        self.skillPointsBox.setValue(52)
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

        self.dcalc = (
            DamageCalculator()
            .with_available_sp(available_sp)
            .with_helmetlvl(helmet)
            .with_chestlvl(chest)
            .with_gloveslvl(gloves)
            .with_pantslvl(pants)
            .with_bootslvl(boots)
            .with_pill(pill)
            .with_ammolvl(bullets)
            .with_weaponlvl(weapon)
            .with_per_hour(per_hour)
            .with_mu_hqlvl(headquarters)
            .with_country_bunkerlvl(country_bunker)
            .with_military_baselvl(military_base)
            .with_country_orderlvl(country_order)
            .with_mu_orderlvl(mu_order)
            .with_resistance(resistance)
            .with_core_region(core_region)
            .with_ally(ally)
            .with_sworn_enemy(sworn_enemy)
            .with_region_not_linked(region_not_linked)
            .with_attacking_region_lost(attacking_region_lost)
        )
        self.dcalc.post_init()
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
        self.damage = QLabel(label)
        self.parameter_layout.addRow("Skill points", self.skillPointsBox)
        self.parameter_layout.addRow("Weapon level", self.weaponBox)
        self.parameter_layout.addRow("Bullets level", self.bulletsBox)
        self.parameter_layout.addRow("Helmet level", self.helmetBox)
        self.parameter_layout.addRow("Chest level", self.chestBox)
        self.parameter_layout.addRow("Gloves level", self.glovesBox)
        self.parameter_layout.addRow("Pants level", self.pantsBox)
        self.parameter_layout.addRow("Boots level", self.bootsBox)
        self.parameter_layout.addRow(
            "Military unit headquarter level", self.headquartersBox
        )
        self.parameter_layout.addRow("Military unit order level", self.muOrderBox)
        self.parameter_layout.addRow("Country order level", self.countryOrderBox)
        self.parameter_layout.addRow("Country bunker level", self.countryBunkerBox)
        self.parameter_layout.addRow("Military base level", self.militaryBaseBox)
        self.parameter_layout.addRow("Resistance level", self.resistanceBox)
        self.parameter_layout.addRow("Pill?", self.pillBox)
        self.parameter_layout.addRow("Ally?", self.allyBox)
        self.parameter_layout.addRow("Sworn Enemy?", self.swornEnemyBox)
        self.parameter_layout.addRow("Core region?", self.coreRegionBox)
        self.parameter_layout.addRow(
            "Attacking region lost?", self.attackingRegionLostBox
        )
        self.parameter_layout.addRow("Region not linked?", self.regionNotLinkedBox)
        self.parameter_layout.addRow(
            "Damage per hour?",
            self.perHourBox,
        )
        self.parameter_layout.addRow("Damage", self.damage)

        self.window_layout.addLayout(self.parameter_layout)
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
        self.damage.setText(self.calc_upgrade())

    def chest_changed(self):
        self.dcalc.set_chest_lvl(self.chestBox.value())
        self.damage.setText(self.calc_upgrade())

    def gloves_changed(self):
        self.dcalc.set_gloves_lvl(self.glovesBox.value())
        self.damage.setText(self.calc_upgrade())

    def pants_changed(self):
        self.dcalc.set_pants_lvl(self.pantsBox.value())
        self.damage.setText(self.calc_upgrade())

    def boots_changed(self):
        self.dcalc.set_boots_lvl(self.bootsBox.value())
        self.damage.setText(self.calc_upgrade())

    def bullets_changed(self):
        self.dcalc.set_ammo_lvl(self.bulletsBox.value())
        self.damage.setText(self.calc_upgrade())

    def weapon_changed(self):
        self.dcalc.set_weapon_lvl(self.weaponBox.value())
        self.damage.setText(self.calc_upgrade())

    def headquarters_changed(self):
        self.dcalc.set_mu_hq_lvl(self.headquartersBox.value())
        self.damage.setText(self.calc_upgrade())

    def mu_order_lvl_changed(self):
        self.dcalc.set_mu_order_lvl(self.muOrderBox.value())
        self.damage.setText(self.calc_upgrade())

    def country_order_lvl_changed(self):
        self.dcalc.set_country_order_lvl(self.countryOrderBox.value())
        self.damage.setText(self.calc_upgrade())

    def country_bunker_lvl_changed(self):
        self.dcalc.set_country_bunker_lvl(self.countryBunkerBox.value())
        self.damage.setText(self.calc_upgrade())

    def military_base_lvl_changed(self):
        self.dcalc.set_military_base_lvl(self.militaryBaseBox.value())
        self.damage.setText(self.calc_upgrade())

    def resistance_lvl_changed(self):
        self.dcalc.set_resistance(self.resistanceBox.value())
        self.damage.setText(self.calc_upgrade())

    def per_hour_changed(self):
        self.dcalc.set_per_hour(self.perHourBox.isChecked())
        self.damage.setText(self.calc_upgrade())

    def pill_changed(self):
        self.dcalc.set_pill(self.pillBox.isChecked())
        self.damage.setText(self.calc_upgrade())

    def ally_changed(self):
        self.dcalc.set_ally(self.allyBox.isChecked())
        self.damage.setText(self.calc_upgrade())

    def sworn_enemy_changed(self):
        self.dcalc.set_sworn_enemy(self.swornEnemyBox.isChecked())
        self.damage.setText(self.calc_upgrade())

    def core_region_changed(self):
        self.dcalc.set_core_region(self.coreRegionBox.isChecked())
        self.damage.setText(self.calc_upgrade())

    def attacking_region_lost_changed(self):
        self.dcalc.set_attacking_region_lost(self.attackingRegionLostBox.isChecked())
        self.damage.setText(self.calc_upgrade())

    def region_not_linked_changed(self):
        self.dcalc.set_region_not_linked(self.regionNotLinkedBox.isChecked())
        self.damage.setText(self.calc_upgrade())

    def sp_changed(self):
        self.dcalc.set_skill_points(self.skillPointsBox.value())
        self.damage.setText(self.calc_upgrade())

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
