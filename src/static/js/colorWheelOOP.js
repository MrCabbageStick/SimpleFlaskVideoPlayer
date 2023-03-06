class SliderObject{

    /**
     * Creates a Slider object
     * @param {HTMLElement} elem
     * @param {(e: PointerEvent) => any} onPress
     * @param {(e: PointerEvent) => any} onRelease
     * @param {(e: PointerEvent) => any} onSlide
     */
    constructor(elem, onPress = null, onRelease = null, onSlide = null, onSetValue = null){
        this.elem = elem;
        this.onPress = onPress ?? this.onPress;
        this.onRelease = onRelease ?? this.onRelease;
        this.onSlide = onSlide ?? this.onSlide;
        this._onSetValue = onSetValue ?? this._onSetValue;

        this.isPressed = false;
        this.value = 0;

        this._registerEvents();
    }

    _registerEvents(){
        let that = this
        this.elem.addEventListener("pointerdown", (e) => {
            that._onPress(e);
        });
        this.elem.addEventListener("pointerup", (e) => {
            that._onRelease(e);
        });
        this.elem.addEventListener("pointerleave", (e) => {
            that._onRelease(e);
        });
        this.elem.addEventListener("pointermove", (e) => {
            that._onSlide(e);
        });
    }

    /**
     * Overwrite me
     * @param {PointerEvent} e
     */
    onPress(e){}
    /**
     * Overwrite me
     * @param {PointerEvent} e
     */
    onRelease(e){}
    /**
     * Overwrite me
     * @param {PointerEvent} e
     */
    onSlide(e){}
    /**
     * Overwrite me
     * @param {number} e
     */
    _onSetValue(value){}

    /**
     * A wrapper for onPress function
     *
     * Do not touch if not necessary
     * @param {PointerEvent} e
     */
    _onPress(e){
        this.isPressed = true;
        this.value = this._getValue(e)
        this.onPress(e);
    }
    /**
     * A wrapper for onRelease function
     *
     * Do not touch if not necessary
     * @param {PointerEvent} e
     */
    _onRelease(e){
        this.isPressed = false;
        this.onRelease(e);
    }
    /**
     * A wrapper for onSlide function
     *
     * Do not touch if not necessary
     * @param {PointerEvent} e
     */
     _onSlide(e){
        if(!this.isPressed) return;
        this.value = this._getValue(e)
        this.onSlide(e);
    }

    /**
     * Overwrite me
     * @param {PointerEvent} e
     */
    _getValue(e){}

    /**
     * Overwrite me
     * @param {number} new_value
     */
    setValue(new_value){
        this.value = new_value;
        this._onSetValue(new_value);
    }

}


class HorizontalSlider extends SliderObject{
    /**
     * Returns value in percents
     * @param {PointerEvent} e
     */
     _getValue(e){
        let slider_elem_pos = this.elem.getBoundingClientRect()
        let relative_mouse_x = e.clientX - slider_elem_pos.x

        if(relative_mouse_x > slider_elem_pos.width) return 100
        if(relative_mouse_x < 0) return 0
        return relative_mouse_x / slider_elem_pos.width * 100
    }
}


class CirclularSlider extends SliderObject{

    /**
     * Returns value in degrees
     * @param {PointerEvent} e
     */
    _getValue(e){
        let wheel_pos = this.elem.getBoundingClientRect()
        let wheel_center = {x: wheel_pos.x + wheel_pos.width / 2, y: wheel_pos.y + wheel_pos.height / 2}

        let relative_mouse_pos = {x: (e.clientX - wheel_center.x), y: (e.clientY - wheel_center.y)}
        if(relative_mouse_pos.x === 0 && relative_mouse_pos.y === 0) relative_mouse_pos = {x: 1, y: 1}

        let angle = (relative_mouse_pos.y >= 0)
                    ? Math.atan(-relative_mouse_pos.x / relative_mouse_pos.y) + Math.PI
                    : Math.atan(relative_mouse_pos.x / -relative_mouse_pos.y)

        // Radians to degrees conversion
        angle = angle * 180 / Math.PI

        return angle
    }
}


class ColorPicker{

    /**
     *
     * @param {HTMLElement} hueSliderElem
     * @param {HTMLElement} saturationSliderElem
     * @param {HTMLElement} lightnessSliderElem
     * @param {(color: {hue: number, saturation: number, lightness: number}) => any} onColorChange
     */
    constructor(hueSliderElem, saturationSliderElem, lightnessSliderElem, onColorChange = null){

        this.onColorChange = onColorChange ?? this.onColorChange;

        this.color = {
            hue: 0,
            saturation: 0,
            lightness: 0,
        };

        this.hueSlider = new CirclularSlider(hueSliderElem)
        this.hueSlider.onPress = () => this._setHue(this.hueSlider.value)
        this.hueSlider.onSlide = () => this._setHue(this.hueSlider.value)


        this.saturationSlider = new HorizontalSlider(saturationSliderElem)
        this.saturationSlider.onPress = () => this._setSaturation(this.saturationSlider.value)
        this.saturationSlider.onSlide = () => this._setSaturation(this.saturationSlider.value)

        this.lightnessSlider = new HorizontalSlider(lightnessSliderElem)
        this.lightnessSlider.onPress = () => this._setLightness(this.lightnessSlider.value)
        this.lightnessSlider.onSlide = () => this._setLightness(this.lightnessSlider.value)


    }


    _setHue(hue){
        this.color.hue = Math.round(hue);
        this._onColorChange();
    }


    _setSaturation(saturation){
        this.color.saturation = Math.round(saturation);
        this._onColorChange();
    }


    _setLightness(lightness){lightness
        this.color.lightness = Math.round(lightness);
        this._onColorChange();
    }

    _onColorChange() {
        this.onColorChange(this.color);
    }

    /**
     * Overwrite me
     * @param {{hue: number, saturation: number, lightness: number}} color
     */
    onColorChange(color){}


    setColor(hue = null, saturation = null, lightness = null){

        this.color.hue = hue ?? this.color.hue;
        this.color.saturation = saturation ?? this.color.saturation;
        this.color.lightness = lightness ?? this.color.lightness;

        this.hueSlider.value = this.color.hue;
        this.saturationSlider.value = this.color.saturation;
        this.lightnessSlider.value = this.color.lightness

        this._onColorChange();
    }

}
