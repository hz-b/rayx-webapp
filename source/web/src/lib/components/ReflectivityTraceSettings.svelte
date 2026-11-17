<script lang="ts">
    import Pane from 'svelte-tweakpane-ui/Pane.svelte';
    import IntervalSlider from 'svelte-tweakpane-ui/IntervalSlider.svelte';
    import Slider from 'svelte-tweakpane-ui/Slider.svelte';
    import Stepper from 'svelte-tweakpane-ui/Stepper.svelte';
    import Text from 'svelte-tweakpane-ui/Text.svelte';
    import Button from 'svelte-tweakpane-ui/Button.svelte';
    import {type Theme } from 'svelte-tweakpane-ui';
    import { HZBColorThemeLight } from './Colors';

    let { endpoint = '/api/trace' }: { endpoint?: string } = $props();

    let energy = $state<[number, number]>([20, 100]);

    let mirror = $state({
        angle: 0,
        material: '',
        density: -1,
        roughness: 1,
        linearPol_0: 0,
        linearPol_45: 0,
        CircularPol: 0
    });

    let sending = $state(false);
    let message = $state('');
    let failed = $state(false);

    function inRange(value: number, min: number, max: number) {
        return Number.isFinite(value) && value >= min && value <= max;
    }

    async function trace() {
        if (sending) return;

        message = '';
        failed = false;

        const valid =
            inRange(energy[0], 0, 1000) &&
            inRange(energy[1], 0, 1000) &&
            energy[0] <= energy[1] &&
            inRange(mirror.angle, -360, 360) &&
            inRange(mirror.density, -1, 100) &&
            inRange(mirror.roughness, 0, 1) &&
            inRange(mirror.linearPol_0, -1, 1) &&
            inRange(mirror.linearPol_45, -1, 1) &&
            inRange(mirror.CircularPol, -1, 1);

        if (!valid) {
            failed = true;
            message = 'Please enter valid numbers within the specified ranges.';
            return;
        }

        const payload = {
            graph: {
                energy_eV: {
                    from: energy[0],
                    to: energy[1]
                }
            },
            mirror: {
                angle_deg: mirror.angle,
                material: mirror.material.trim(),
                density: mirror.density,
                roughness: mirror.roughness,
                linearPol_0: mirror.linearPol_0,
                linearPol_45: mirror.linearPol_45,
                CircularPol: mirror.CircularPol
            }
        };

        sending = true;

        try {
            const response = await fetch(endpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(payload)
            });

            if (!response.ok) {
                throw new Error(`Trace request failed (HTTP ${response.status}).`);
            }

            message = 'Trace request accepted.';
        } catch (error) {
            failed = true;
            message =
                error instanceof Error
                    ? error.message
                    : 'Unable to send the trace request.';
        } finally {
            sending = false;
        }
    }

    const settingsTheme: Theme = {

        // Overall appearance
        baseBackgroundColor: 'transparent',
        baseShadowColor: 'transparent',
        baseFontFamily: 'Roboto, sans-serif',
        baseBorderRadius: '8px',

        // Control shape and layout
        bladeBorderRadius: '5px',
        bladeHorizontalPadding: '8px',
        bladeValueWidth: '50%',

        // Headers and spacing
        containerHorizontalPadding: '8px',
        containerVerticalPadding: '8px',
        containerUnitSize: '28px',
        containerUnitSpacing: '8px',

        // Labels
        labelForegroundColor: '#475569',

        // Inputs
        inputBackgroundColor: "transparent",
        inputBackgroundColorHover: HZBColorThemeLight.input_field_hover,
        inputBackgroundColorFocus: HZBColorThemeLight.input_field_focus,
        inputBackgroundColorActive: HZBColorThemeLight.input_field_focus,
        inputForegroundColor: HZBColorThemeLight.text_on_white,

        // Slider tracks
        grooveForegroundColor: HZBColorThemeLight.primary,

        // Buttons
        buttonBackgroundColor: HZBColorThemeLight.primary,
        buttonBackgroundColorHover: HZBColorThemeLight.secondary,
        buttonBackgroundColorFocus: HZBColorThemeLight.secondary,
        buttonBackgroundColorActive: HZBColorThemeLight.third_option,
        buttonForegroundColor: HZBColorThemeLight.text_on_black
    };
</script>

<div class="trace-settings" aria-busy={sending}>
        <h3>Graph Settings</h3>
        <Pane position="inline" theme={settingsTheme}>
            <IntervalSlider
                label="eV"
                bind:value={energy}
                min={0}
                max={1000}
                step={1}
            />
        </Pane>

        <h3>Mirror Settings</h3>
        <Pane position="inline" theme={settingsTheme}>
        <Slider
            label="Angle (°)"
            bind:value={mirror.angle}
            min={-360}
            max={360}
            step={0.01}
        />
        <Text label="Material" bind:value={mirror.material} />
        <Stepper
            label="Density"
            bind:value={mirror.density}
            min={-1}
            max={100}
            step={0.01}
        />
        <Stepper
            label="Roughness"
            bind:value={mirror.roughness}
            min={0}
            max={1}
            step={0.01}
        />
        <Stepper
            label="linearPol_0"
            bind:value={mirror.linearPol_0}
            min={-1}
            max={1}
            step={0.01}
        />
        <Stepper
            label="linearPol_45"
            bind:value={mirror.linearPol_45}
            min={-1}
            max={1}
            step={0.01}
        />
        <Stepper
            label="CircularPol"
            bind:value={mirror.CircularPol}
            min={-1}
            max={1}
            step={0.01}
        />

        <Button
            title={sending ? 'Sending…' : 'Trace'}
            disabled={sending}
            on:click={trace}
        />
    </Pane>

    <p role="status" class:error={failed}>{message}</p>
</div>

<style>
    .trace-settings {
        width: 100%;
        min-width: 0;
        overflow: hidden;
    }

    /* Label */
    .trace-settings h3{
        font-size: var(--average-settings-label-size);
        color: var(--color-text-on-black);
        background: var(--color-label-backdrop);
        padding: 0.2rem;
    }

    /* Input Label and Input */
    .trace-settings :global(.tp-lblv_l),
    .trace-settings :global(input){
        font-size: var(--average-text-size);
    }

    .trace-settings :global(.tp-txtv_i) {
        border: 1px solid var(--color-input-field-color);
        border-radius: 0;
    }

    .trace-settings :global(.tp-btnv_t) {
        font-size: var(--average-text-size);
    }

    p {
        margin: 0.75rem 0 0;
        font-size: 0.875rem;
    }

    p:empty {
        display: none;
    }

    .error {
        color: #dc2626;
    }
</style>
