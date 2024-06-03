# Copyright (c) [2024] [Sebastian Kliem]

class Calculate_Steam:
    """
    Calculates the amount of Water that is used.
    """

    def __init__(self,
                 temperature: int,
                 humitidy: int,
                 max_flow: int,
                 celsius: bool = True,
                 high_temperature: bool = False,
                 calculation_method_correction: bool = False):


        self._humitidy: int = humitidy
        self._max_flow: int = max_flow
        self._high_temperature: bool = high_temperature
        self._calculation_method_correction = calculation_method_correction

        self._milliliter_per_minute: float = 0.0
        self._liter_in_hour: float = 0.0
        self._set_temperature(temperature=temperature,
                              celsius=celsius)

        self.calculate_amount_of_water()

    def calculate_amount_of_water(self):
        """
        Calculate the amount of water that is used.
        :return:
        """

        factor: float = self._start_calculation() / 10
        self._milliliter_per_minute = ((self._max_flow / 60) * 1000) * (factor / 100)
        self._liter_in_hour = int((round(self._milliliter_per_minute, 2) * 60)) / 1000

    def _set_temperature(self, temperature: int, celsius: bool) -> None:
        """
        Set the given temperature in Celsius.
        :param temperature:
        :return:
        """

        if celsius:
            self._temperature: float = temperature
            return

        temperature_in_celsius: float = (temperature - 32) / 1.8
        self._temperature: float = temperature_in_celsius
        return

    def _start_calculation(self) -> float:
        """
        Starts the calculation to get the faktor.
        :return:
        """
        # in these cases, no water is used:
        if not self._high_temperature and self._temperature > 230:
            return 0.0

        if self._high_temperature and self._temperature > 330:
            return 0.0

        return self._select_formula_cooking()

    def _select_formula_cooking(self) -> float:
        """
        Select the right calculation method for mode cooking
        :return:
        """

        if self._calculation_method_correction and self._humitidy < 20:
            if self._temperature <= 120:
                return self._calc_very_low_humidity_low_temperature()

            if self._temperature > 120:
                return self._calc_very_low_humidity_high_temperature()

        elif self._humitidy < 90:
            if self._temperature <= 120:
                return self._calc_low_humidity_low_temperature()

            if self._temperature > 120:
                return self._calc_low_humidity_high_temperature()

        elif self._humitidy >= 90:
            if self._temperature < 110:
                return self._calc_high_humidity_low_temperature()

            if 110 <= self._temperature < 120:
                return self._calc_high_humidity_middle_temperature()

            if self._temperature >= 120:
                return self._calc_high_humidity_high_temperature()

    def _calc_very_low_humidity_low_temperature(self) -> float:
        """
        Calculate the used water when huminidy less than 20 percent and low temperature are set.
        :return:
        """

        return ((self._humitidy - 1) * 10 * 35) / 39

    def _calc_very_low_humidity_high_temperature(self) -> float:
        """
        Calculate the used water when huminidy less than 20 and high temperature are set.
        :return:
        """

        calc_part_one = self._calc_very_low_humidity_low_temperature()

        if self._high_temperature:
            return calc_part_one * ((330 - self._temperature) / 210)

        return calc_part_one * ((230 - self._temperature) / 110)

    def _calc_low_humidity_low_temperature(self) -> float:
        """
        Calculate the used water when low huminidy and low temperature are set.
        :return:
        """

        if self._calculation_method_correction:
            return ((self._humitidy - 15) / 75) * 675
        return (self._humitidy / 90) * 675

    def _calc_low_humidity_high_temperature(self) -> float:
        """
        Calculate the used water when low huminidy and high temperature are set.
        :return:
        """

        calc_part_one = self._calc_low_humidity_low_temperature()

        if self._high_temperature:
            return calc_part_one * ((330 - self._temperature) / 210)

        return calc_part_one * ((230 - self._temperature) / 110)

    def _calc_high_humidity_low_temperature(self) -> float:
        """
        Calculate the used water when high huminidy and low temperature are set.
        :return:
        """

        return 325 * ((self._humitidy - 90) / 10) + 675

    def _calc_high_humidity_middle_temperature(self) -> float:
        """
        Calculate the used water when high huminidy and middle temperature are set.
        :return:
        """

        calc_part_one = self._calc_high_humidity_low_temperature()

        calc_part_two = 75 * ((self._humitidy - 90) / 10) + 675

        return (calc_part_one - calc_part_two) * ((120 - self._temperature) / 10) + calc_part_two

    def _calc_high_humidity_high_temperature(self) -> float:
        """
        Calculate the used water when high huminidy and high temperature are set.
        :return:
        """

        calc_part_one = 75 * ((self._humitidy - 90) / 10) + 675

        if self._high_temperature:
            return calc_part_one * ((330 - self._temperature) / 210)

        return calc_part_one * ((230 - self._temperature) / 110)

    def get_amount_of_water(self) -> list:
        """
        Returns the amount of water used in milliliter per minute.
        :return:
        """

        return [round(self._milliliter_per_minute, 2), self._liter_in_hour]
